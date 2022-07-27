import os
import sys
from .secret_utils import get_secret, get_s3_credentials

from .exec_utils import is_job_running_on_server

OUTPUT_FILES_DIR = os.environ.get("HYPERPLANE_USER_OUTPUTS_DIR", os.getcwd())
OUTPUT_FILES_DIR_ABS = os.environ.get("HYPERPLANE_USER_OUTPUTS_DIR_ABS", os.getcwd())


def get_env_param(env_param):
    if is_job_running_on_server():
        return None
    return os.environ.get(env_param)


def get_job_id():
    job_id = os.environ.get('HYPERPLANE_JOB_ID')

    if not job_id:
        print("Warning: job_id is None. Please set HYPERPLANE_JOB_ID env var")

    return job_id


def get_user_id():
    user_id = os.environ.get('HYPERPLANE_USER_ID')

    if not user_id:
        print("Warning: user_id is None. Please set HYPERPLANE_USER_ID env var")

    return user_id


def report(analytics_str):
    if is_job_running_on_server():
        sys.path.append("..")
        from hyperplane_server_utils import report
        return report(analytics_str)

    print(f"REPORTED: {analytics_str}")

    return True


def print_to_file(out_file_name, *payloads):
    output_files_abs_path = "."  # current directory
    if is_job_running_on_server():
        output_files_abs_path = os.environ.get("HYPERPLANE_USER_OUTPUTS_DIR_ABS", os.getcwd())
    with open(f"{output_files_abs_path}/{out_file_name}", "a") as f:
        for p in payloads:
            f.write(p)
