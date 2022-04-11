import requests
import sys
import os
import json

OUTPUT_FILES_BASE_DIR = "outputs"
ANALYTICS_API_NAME = "report"
SECRETS_API_NAME = "secrets"
SET_JOB_STATUS_API_NAME = "set_job_status"


def __report_test_api_fail(api_name, api_spec, response):
    if os.environ.get("HYPERPLANE_TEST_MODE_TRUE"):
        print(f"Failed to fetch key from {api_name} with parameters: "
              f"{api_spec.get('method')}, {api_spec.get('url')}",
              f" and headers: "
              f"{api_spec.get('headers')}",
              f" and got the response: "
              f"{response} "
              f"(response code:{response.status_code})",
              file=sys.stderr)


def __get_api_spec(api_spec_name, url_params=None):
    if url_params is None:
        url_params = dict()

    api_specs = {
        SECRETS_API_NAME: {
            "url": "https://pe4exfipne.execute-api.eu-central-1.amazonaws.com/default/GetSecretByKey",
            "params": {
                "userid": url_params.get("user_id"),
                "secretname": url_params.get(url_params.get("secret_name"), "key"),
            },
            "method": "GET",
            "api_key": os.environ.get('HYPERPLANE_SECRETS_API_KEY'),
            "Content-Type": "text/plain",
        },
        ANALYTICS_API_NAME: {
            "url": "https://4nix3yd9ga.execute-api.eu-central-1.amazonaws.com/default/ChangeJobStatusFromApplication",
            "method": "PUT",
            "api_key": os.environ.get('HYPERPLANE_ANALYTICS_API_KEY'),
            "Content-Type": "text/plain",
        },
        SET_JOB_STATUS_API_NAME: {
            "url": "https://4nix3yd9ga.execute-api.eu-central-1.amazonaws.com/default/SetJobStatus",
            "params": {
                "job_id": url_params.get("job_id"),
            },
            "method": "PUT",
            "api_key": os.environ.get('HYPERPLANE_SET_JOB_STATUS_API_KEY'),
            "Content-Type": "text/plain",
        },
    }

    spec = api_specs.get(api_spec_name)

    # generate headers (if a valid spec was requested)
    if spec is not None:
        spec["headers"] = {}
        content_type = spec.get('Content-Type')
        if content_type is not None:
            spec["headers"]['Content-Type'] = content_type

        api_key = spec.get("api_key")
        if api_key is not None:
            spec["headers"]['X-API-Key'] = api_key

    return spec


def send_api_call(api_name, data=None, url_params=None, json_response=True):
    api_spec = __get_api_spec(api_name, url_params)
    response = requests.request(api_spec.get("method"),
                                api_spec.get("url"),
                                params=api_spec.get("params"),
                                headers=api_spec.get("headers"),
                                data=data)

    if response.status_code == 200:
        if json_response:
            return json.loads(response.text)
        return response.text
    __report_test_api_fail(api_name, api_spec, response)
    return None
