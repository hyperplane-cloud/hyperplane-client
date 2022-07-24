import os
import sys


from .exec_utils import is_job_running_on_server


def get_secret(secret_name):
    if is_job_running_on_server():
        sys.path.append("..")
        from hyperplane_server_utils import get_secret
        return get_secret(secret_name)

    secret = os.environ.get(secret_name)

    if secret is None:
        raise ValueError(f'Environment variable: {secret_name} is not set for local run')

    return secret


def get_s3_credentials() -> dict:
    """ Return a dict with 3 keys:
    access_key_id, secret_access_key, bucket_url
    """

    access_key_id = get_secret("s3_access_key_id")
    secret_access_key = get_secret("s3_access_key_secret")
    bucket_url = get_secret("s3_bucket_name")

    return {
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
        "bucket_url": bucket_url,
    }

