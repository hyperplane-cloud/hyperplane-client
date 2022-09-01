import os
import sys
from typing import Optional

from .exec_utils import is_job_running_on_server


def get_secret(secret_name: str) -> Optional[str]:
    if is_job_running_on_server():
        if ".." not in sys.path:
            sys.path.append("..")
        from get_user_secret import get_user_secret as get_secret_from_server
        return get_secret_from_server(secret_name)

    else:
        secret_env_var = f"HYPERPLANE_SECRET_{secret_name}"
        secret_value = os.getenv(secret_env_var)

        if not secret_value:
            print(f"Warning: {secret_name} is not set. You can set it locally by setting the {secret_env_var} environment variable")

        return secret_value


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

