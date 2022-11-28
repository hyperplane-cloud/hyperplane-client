import os
import re
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from hyperplane import get_s3_credentials, report


def _get_s3_connector(bucket_name, user_s3_creds, access_key_secret=None, access_key_id=None):
    print(f"Connecting s3 bucket: {bucket_name}")

    if not access_key_id or not access_key_secret:
        print("Connecting to s3 bucket with stored access key id and secret access key")
        user_bucket_name = user_s3_creds.get("bucket_url")
        if bucket_name == user_bucket_name:
            if not access_key_secret:
                access_key_secret = user_s3_creds.get("secret_access_key")
            if not access_key_id:
                access_key_id = user_s3_creds.get("access_key_id")

    connector = boto3
    if access_key_id and access_key_secret:
        connector = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=access_key_secret)

    return connector


def download_from_s3(source_path: str, target_path: str = None, regex_filter: str = None):
    """
    Args:
        source_path: for directories put '/' in the end
        target_path: for dir: Should end with '/'. files from source_path dir will be uploaded under target_path.
                     for file: where the file will be saved (including name).
        regex_filter: filter by regex
    """
    user_s3_creds = get_s3_credentials()

    bucket_name = user_s3_creds.get("bucket_url")
    if not bucket_name:
        report("User didn't specify bucket name and have no bucket configurations in our system")
        return None
    s3_connector = _get_s3_connector(bucket_name=bucket_name, user_s3_creds=user_s3_creds)
    s3_resource = s3_connector.resource('s3')

    bucket = s3_resource.Bucket(bucket_name)
    objects_to_download = list(bucket.objects.filter(Prefix=source_path))
    regex_compile = re.compile(regex_filter) if regex_filter else None

    for obj in objects_to_download:
        relpath_to_source = os.path.relpath(obj.key, source_path)
        if regex_compile and not regex_compile.search(relpath_to_source):
            continue

        if not target_path or target_path == '.':
            # if target path is not mentioned, store as in the bucket root, keep original files` hierarchy.
            target_name = relpath_to_source
        elif target_path.endswith('/'):
            # target path is a dir, keep original files` hierarchy.
            target_name = target_path + relpath_to_source
        else:
            # uploading file to a specific target
            target_name = target_path

        dir_to = os.path.dirname(target_name)
        Path(dir_to).mkdir(parents=True, exist_ok=True)

        bucket.download_file(obj.key, target_name)


def upload_to_s3(source_path: str, target_path: str = None, regex_filter: str = None, verbose: bool = True):
    """
    Upload source path to {bucket}/{target_path}
    Args:
        source_path: if a directory, all files and directories under source_path will be upload recursively under target_path
        target_path: full target path including desired file name for files and directory name for directory.
        regex_filter: if not None, only filename that matches this pattern will be uploaded
        bucket_name: bucket name to upload
        verbose: show prints
    Returns:
        None
    """
    user_s3_creds = get_s3_credentials()
    bucket_name = user_s3_creds.get("bucket_url")
    if not bucket_name:
        report("User didn't specify bucket name and have no bucket configurations in our system")
        return None
    s3_connector = _get_s3_connector(bucket_name=bucket_name, user_s3_creds=user_s3_creds)
    s3_client = s3_connector.client('s3')
    regex_filter_compiled = None
    if regex_filter:
        regex_filter_compiled = re.compile(regex_filter)
    if os.path.isfile(source_path):
        if verbose:
            print('uploading file to s3')
        return _upload_file_to_s3(file_path=source_path, bucket=bucket_name, object_name=target_path,
                                  regex_filter=regex_filter_compiled, s3_client=s3_client, verbose=verbose)
    elif os.path.isdir(source_path):
        if verbose:
            print('uploading dir to s3')
        return _upload_directory_to_s3(local_base_directory=source_path, bucket=bucket_name,
                                       s3_base_directory=target_path,
                                       regex_filter=regex_filter_compiled, s3_client=s3_client, verbose=verbose)


def _upload_file_to_s3(file_path, bucket, s3_client, object_name=None, extra_args=None, verbose=False,
                       regex_filter: re.Pattern = None):
    """Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :param extra_args: arg to pass to s3 call
    :param verbose: print logs if true
    :param regex_filter: regex compile str to match
    :param s3_client: s3 client to interact with the bucket
    :return: s3 url if file was uploaded, else None

    """
    if regex_filter:
        if regex_filter.search(file_path) is None:
            if verbose:
                print(f'File: {file_path} will not be uploaded since it doesnt match the filter')
            return None

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Upload the file
    if verbose:
        print(f'Uploading {file_path} as {bucket}/{object_name}')
    try:
        s3_client.upload_file(file_path, bucket, object_name, extra_args)
        if verbose:
            print(f'  {object_name}: Upload Successful')
    except NoCredentialsError:
        if verbose:
            print("Credentials not available")
        return None
    except ClientError as e:
        if verbose:
            print(f"Failed with error: {str(e)}")
        return None
    region = s3_client.get_bucket_location(Bucket=bucket)['LocationConstraint']
    if region is None:
        region = s3_client.meta.region_name
    return f"https://{bucket}.s3.{region}.amazonaws.com/{object_name}"


def _upload_directory_to_s3(local_base_directory, s3_client, bucket, s3_base_directory, extra_args=None, verbose=False,
                            regex_filter: re.Pattern = None,):
    file_urls = []
    walks = os.walk(local_base_directory)
    for current_directory, dirs, files in walks:
        if verbose:
            print(f'Directory: {current_directory}:')
        for filename in files:
            # construct the full local path
            local_file = os.path.join(current_directory, filename)
            # construct the full s3 path
            relative_path = os.path.relpath(local_file, local_base_directory)
            if s3_base_directory:
                s3_object_name = os.path.join(s3_base_directory, relative_path)
            else:
                s3_object_name = relative_path
            # Invoke upload function
            s3_file_url = _upload_file_to_s3(file_path=local_file, bucket=bucket, object_name=s3_object_name,
                                             extra_args=extra_args, verbose=verbose, regex_filter=regex_filter,
                                             s3_client=s3_client)
            if s3_file_url:
                file_urls.append(s3_file_url)
    return file_urls
