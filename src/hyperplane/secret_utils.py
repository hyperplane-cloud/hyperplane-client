import os
import sys
from typing import Optional

from .exec_utils import is_job_running_on_server


def get_secret(secret_name: str) -> Optional[str]:
    if is_job_running_on_server():
        sys.path.append("..")
        from hyperplane_server_utils import get_secret
        return get_secret(secret_name)

    user_token = os.getenv("HYPERPLANE_USER_TOKEN")

    if user_token:
        sys.path.append("..")
        from hyperplane_server_utils import get_secret_by_user_token  #how does this import will work in the user computer?
        return get_secret_by_user_token(secret_name, user_token)

    return os.getenv(f"HYPERPLANE_SECRET_{secret_name}")


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

