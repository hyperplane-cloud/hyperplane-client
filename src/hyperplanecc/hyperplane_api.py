# hyperplane_api.py - hyperplane api class

import os
from backend import *
from job import Job


class hyperplane_api(object):
    def __init__(self):
        self.api_token = None

    def connect(self, api_token: str = None):
        if api_token:
            self.api_token = api_token
        else:
            self.api_token = os.getenv('HYPERPLANE_API_TOKEN')
        if not api_token:
            print(f"Could not find environment variable HYPERPLANE_API_TOKEN.")
            return None
        return self

    def get_all_jobs(self):
        jobs = call_backend(
            api_url=API_GetAllJobs,
            method=METHOD_GET,
            api_token=self.api_token,
            )
        if jobs is None:
            return None
        jobs = [Job(job) for job in jobs]
        return jobs

    def get_job(self, job_id: str):
        job = call_backend(
            api_url=API_GetJobById,
            method=METHOD_GET,
            api_token=self.api_token,
            params={'ID': job_id},
            )
        if job is None:
            return None
        return Job(job)

    def create_job(self, job_name: str = "", git_repo_url: str = "",
                   branch_name: str = "", hyperplane_config: str = "",
                   instance_type: str = "", instance_count: str = ""):
        new_job = call_backend(
            api_url=API_CreateJob,
            method=METHOD_POST,
            api_token=self.api_token,
            jobName=job_name,
            instanceType=instance_type,
            gitRepoUrl=git_repo_url,
            hyperplaneConfig=hyperplane_config,
            instance_count=instance_count,
            branch_name=branch_name,
            )
        return new_job

    def abort_job(self, job_id: str):
        result = call_backend(
            api_url=API_AbortRunningJob,
            method=METHOD_PATCH,
            api_token=self.api_token,
            job_id=job_id,
            )
        return result == f"Job {job_id} Stopped"

    def create_secret(self, secret_name: str, secret_value: str):
        result = call_backend(
            api_url=API_CreateSecret,
            method=METHOD_POST,
            api_token=self.api_token,
            secret_name=secret_name,
            secret_value=secret_value,
            secret_category="Hyperplane.Access.Tokens",
            )
        return result == f"Created {secret_name} successfully!"
