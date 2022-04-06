import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os


def upload_file_to_s3(file_name, bucket, object_name=None, extra_args=None, verbose=False):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: s3 url if file was uploaded, else None
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    if verbose:
        print(f'  Uploading {file_name} as {bucket}/{object_name}')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, extra_args)
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
    return f"https://{bucket}.s3.{region}.amazonaws.com/{object_name}"


def upload_directory_to_s3(local_base_directory, bucket, s3_base_directory, extra_args=None, verbose=False):
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
            s3_object_name = os.path.join(s3_base_directory, relative_path)
            # Invoke upload function
            s3_file_url = upload_file_to_s3(local_file, bucket, s3_object_name, extra_args=extra_args, verbose=verbose)
            if s3_file_url:
                file_urls.append(s3_file_url)
    return file_urls
