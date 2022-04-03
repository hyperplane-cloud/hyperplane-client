import requests
import json
import os
import sys


OUTPUT_FILES_BASE_DIR = "./outputs/"


def api_fail(api_name, api_spec, response):
    if os.environ.get("HYPERPLANE_TEST_MODE_TRUE"):
        print(f"Failed to fetch key from {api_name} with parameters: {api_spec.get('method')}, {api_spec.get('url')}",
              f" and headers: {api_spec.get('headers')}",
              " and got the response: ", response.status_code, response,
              file=sys.stderr)


def generate_headers(api_spec: dict) -> dict:
    headers = {}

    content_type = api_spec.get('Content-Type')
    if content_type is not None:
        headers['Content-Type'] = content_type

    api_key = api_spec.get("api_key")
    if api_key is not None:
        headers['X-API-Key'] = api_key

    return headers


def get_api_params(api_spec_name, user_id="", job_id="", key=""):
    api_specs = {
        "secrets": {
            "url": f"https://pe4exfipne.execute-api.eu-central-1.amazonaws.com/default/GetSecretByKey?userid={user_id}&secretname={key}",
            "method": "GET",
            "api_key": os.environ.get('HYPERPLANE_SECRETS_API_KEY'),
            "Content-Type": "text/plain",
        },
        "analytics": {
            "url": "https://4nix3yd9ga.execute-api.eu-central-1.amazonaws.com/default/ChangeJobStatusFromApplication",
            "method": "PUT",
            "api_key": os.environ.get('HYPERPLANE_ANALYTICS_API_KEY'),
            "Content-Type": "text/plain",
        },
    }
    spec = api_specs.get(api_spec_name)
    if spec is not None:
        spec["headers"] = generate_headers(spec)
    return spec


def get_env_param(env_param):
    if env_param.startswith("HYPERPLANE_"):
        return None
    return os.environ.get(env_param)


def get_job_id():
    return os.environ.get('HYPERPLANE_JOB_ID')


def get_user_id():
    return os.environ.get('HYPERPLANE_USER_ID')


def get_secret(key):

    api_spec = get_api_params("secrets", user_id=get_user_id(), key=key)

    response = requests.request(api_spec.get("method"),
                                api_spec.get("url"),
                                headers=api_spec.get("headers"),
                                )
    response_obj = json.loads(response.text)

    if response.status_code == 200:
        return response_obj
    api_fail("secrets", api_spec, response)
    return None


def report(analytics_str):
    api_spec = get_api_params("analytics")

    payload = {
        "jobID": get_job_id(),
        "appAnalytics": analytics_str,
    }

    response = requests.request(api_spec.get("method"),
                                api_spec.get("url"),
                                headers=api_spec.get("headers"),
                                data=json.dumps(payload))
    if response.status_code == 200:
        return True
    api_fail("report", api_spec, response)
    return False


def print_to_file(out_file_name, *payloads):
    with open(OUTPUT_FILES_BASE_DIR + out_file_name, "a") as f:
        for p in payloads:
            f.write(p)

