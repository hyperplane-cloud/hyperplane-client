# call_backend.py - backend api

import json
import logging
import requests

BACKEND_URL = "https://api.tons.ai"
SECRETS_BACKEND_URL = "https://api.secrets.tons.ai"

API_GetAllJobs = f"{BACKEND_URL}/jobs/GetJobs"
API_CreateJob = f"{BACKEND_URL}/jobs/CreateJob"
API_GetJobById = f"{BACKEND_URL}/jobs/GetJobByID"
API_AbortRunningJob = f"{BACKEND_URL}/jobs/AbortRunningJob"

API_CreateSecret = f"{SECRETS_BACKEND_URL}/secrets/CreateSecret"

METHOD_GET = "GET"
METHOD_PATCH = "PATCH"
METHOD_POST = "POST"


def call_backend(api_url: str = None, method: str = None, api_token: str = None, params: dict = None, **kwargs) -> dict:
    data = json.dumps({**kwargs})
    headers = {
        "Authorization": f"Bearer {api_token}",
        'Content-Type': 'application/json',
    }
    response = requests.request(method, api_url, params=params, headers=headers, data=data)

    if response.status_code == 200:
        try:
            return json.loads(response.text)
        except Exception as e:
            return response.text
    logging.error(f"Failed to invoke {api_url}. Response {response}.")
    return None
