# job.py - job object
from datetime import datetime

from hyperplane_definitions.job_consts import ACTIVE_JOB_STATES


class Job(object):
    def __init__(self, job_dict: dict):
        self.job_dict = job_dict
        self.id = job_dict.get('ID')
        self.status = job_dict.get('job_status')
        self.creation_time = job_dict.get('creation_time')
        self.start_time = datetime.fromisoformat(self.creation_time)
        self.job_name = job_dict.get('job_name')
        self.git_repo_url = job_dict.get('gitRepoUrl')
        self.instance_type = job_dict.get('instance_type')
        self.hyperplane_config = job_dict.get('hyperplaneConfig')
        self.instance_count = job_dict.get('instance_count')
        self.branch_name = job_dict.get('branch_name')
        self.latest_apm = job_dict.get('application_analytics')

    def __repr__(self) -> str:
        return f"Job {self.id} [{self.status}] {self.job_name} on {self.instance_type}"

    def is_active(self) -> bool:
        return self.status in ACTIVE_JOB_STATES
