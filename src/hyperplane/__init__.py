import os
import sys
from .secret_utils import get_secret, get_s3_credentials
from .exec_utils import is_job_running_on_server
from hyperplane_definitions import get_job_id

OUTPUT_FILES_DIR = os.environ.get("HYPERPLANE_USER_OUTPUTS_DIR", os.getcwd())
OUTPUT_FILES_DIR_ABS = os.environ.get("HYPERPLANE_USER_OUTPUTS_DIR_ABS", os.getcwd())


def get_env_param(env_param):
    if env_param.startswith("HYPERPLANE_"):
        return None
    return os.environ.get(env_param)


def get_user_id():
    user_id = os.environ.get('HYPERPLANE_USER_ID')

    if not user_id:
        print("Warning: user_id is not set, returning None. If needed you can set it via the HYPERPLANE_USER_ID environment variable")

    return user_id


def report(analytics_str):
    if is_job_running_on_server():
        if "/" not in sys.path:
            sys.path.append("/")
        from report_apm import report as report_from_server
        return report_from_server(analytics_str)

    else: # running locally 
        print(f"REPORTED: {analytics_str}")

    return True


def print_to_file(out_file_name, *payloads):
    output_files_base_path = "."  # current directory
    if is_job_running_on_server():
        output_files_base_path = os.environ.get("HYPERPLANE_USER_OUTPUTS_DIR_ABS", os.getcwd())

    output_file_path = os.path.join(output_files_base_path, out_file_name)
    # Make sure dir exists
    output_files_parent_dir_path = os.path.dirname(output_file_path)
    os.makedirs(output_files_parent_dir_path, exist_ok=True)

    with open(output_file_path, "a") as f:
        for p in payloads:
            f.write(p)
