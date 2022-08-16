# job.py - job object

from enum import Enum


class JobStatus(Enum):
    Queued = "Queued"
    Starting = "Starting"
    InProgress = "In Progress"
    Cancelled = "Cancelled"
    Done = "Done"
    Failed = "Failed"


class Job(object):
    def __init__(self, job_dict: dict):
        self.id = job_dict.get('ID')
        self.status = job_dict.get('job_status')
        self.creation_time = job_dict.get('creation_time')
        self.job_name = job_dict.get('job_name')
        self.git_repo_url = job_dict.get('gitRepoUrl')
        self.instance_type = job_dict.get('instanceType')
        self.hyperplane_config = job_dict.get('hyperplaneConfig')
        self.instance_count = job_dict.get('instance_count')
        self.branch_name = job_dict.get('branch_name')
