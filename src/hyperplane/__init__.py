import json
import os

from low_level import send_api_call, OUTPUT_FILES_BASE_DIR, ANALYTICS_API_NAME, SECRETS_API_NAME


def get_env_param(env_param):
    if env_param.startswith("HYPERPLANE_"):
        return None
    return os.environ.get(env_param)


def get_job_id():
    return os.environ.get('HYPERPLANE_JOB_ID')


def get_user_id():
    return os.environ.get('HYPERPLANE_USER_ID')


def get_secret(secret_name):
    api_params = dict(user_id=get_user_id(), secret_name=secret_name)
    return send_api_call(SECRETS_API_NAME, url_params=api_params)


def report(analytics_str):
    payload = {
        "jobID": get_job_id(),
        "appAnalytics": analytics_str,
    }
    data = json.dumps(payload)
    return send_api_call(ANALYTICS_API_NAME, data=data) is not None


def print_to_file(out_file_name, *payloads):
    with open(f"{OUTPUT_FILES_BASE_DIR}/{out_file_name}", "a") as f:
        for p in payloads:
            f.write(p)

