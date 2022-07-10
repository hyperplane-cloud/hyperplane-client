import os
import sys

def get_secret(secret_name):
    if os.environ.get("HYPERPLANE_JOB_ID"):
        # On a server
        sys.path.append("..")
        from hyperplane_server_utils import get_secret
        return get_secret(secret_name)

    # running locally
    return os.environ.get(secret_name)


def get_s3_credentials() -> dict:
    ''' Return a dict with 3 keys:
    access_key_id, secret_access_key, bucket_url
    '''

    access_key_id = get_secret("s3_access_key_id")
    secret_access_key = get_secret("s3_access_key_secret")
    bucket_url = get_secret("s3_bucket_name")

    return {
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
        "bucket_url": bucket_url,
    }

