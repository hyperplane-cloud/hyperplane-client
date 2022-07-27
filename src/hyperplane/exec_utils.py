import os


def is_job_running_on_server() -> bool:
    return os.getenv("IS_RUNNING_ON_SERVER") is not None
