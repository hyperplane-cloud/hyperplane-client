import os


OUTPUT_FILES_BASE_DIR_ABS_PATH = os.environ.get("HYPERPLANE_USER_OUTPUTS_DIR", os.getcwd())


def get_env_param(env_param):
    if env_param.startswith("HYPERPLANE_"):
        return None
    return os.environ.get(env_param)


def get_job_id():
    return os.environ.get('HYPERPLANE_JOB_ID')


def get_user_id():
    return os.environ.get('HYPERPLANE_USER_ID')


def get_secret(secret_name):
    if os.environ.get("HYPERPLANE_JOB_ID"):
        # On a server
        from hyperplane_server_utils import get_secret
        return get_secret(secret_name)

    # running locally
    return os.environ.get(secret_name)


def report(analytics_str):
    if os.environ.get("HYPERPLANE_JOB_ID"):
        # On a server
        from hyperplane_server_utils import report
        return report(analytics_str)

    # running locally
    return print(f"REPORTED: {analytics_str}")


def print_to_file(out_file_name, *payloads):
    with open(f"{OUTPUT_FILES_BASE_DIR_ABS_PATH}/{out_file_name}", "a") as f:
        for p in payloads:
            f.write(p)

