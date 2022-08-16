# sample.py - use hyperplane_api to get list of jobs

from hyperplane_api import hyperplane_api

hapi = hyperplane_api().connect(api_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMzVhYmE1NDc5ZGU2NGFkYjk4NjIyNjg3ODg1OGZhMGQiLCJncm91cF9pZCI6Ijg5MmQwMjU1LTY1YWEtNDVlNi1hY2JmLTg4ZWNjZWM0OTUxNCIsIm9yZ2FuaXphdGlvbl9uYW1lIjoiaHlwZXJwbGFuZSIsImVtYWlsIjoieWFpckBoeXBlcnBsYW5lLmNsb3VkIiwiaWF0IjoxNjYwNjM2OTkwLCJleHAiOjE2NjA2NjU3OTAsImlzcyI6Imh5cGVycGxhbmUiLCJ0b2tlbl9uYW1lIjoic2Vzc2lvbiJ9.Bj6s5zb4PECZPyIjCuvOIaLmNhr-3thSlpslUDkZyDI")

new_job = hapi.create_job(job_name="hapi job",
                          git_repo_url="https://github.com/hyperplane-cloud/hyperplane-lib-demo",
                          instance_type="t2.micro",
                          instance_count="1",
                          hyperplane_config="",
                          branch_name="",
                         )
job_id = None
if isinstance(new_job, dict) and 'job_id' in new_job:
    job_id = new_job['job_id']
    print(f"Created job {job_id}")
else:
    print("Failed to create new job {new_job}")

if job_id:
    status = hapi.abort_job(job_id)
    if status:
        print(f"Aborted job {job_id}")
    else:
        print(f"Failed to abort {job_id}")

jobs = hapi.get_all_jobs()

if not jobs:
    print("Get all jobs failed. Check log.")
else:
    print(f"Found {len(jobs)} jobs")
    for job in jobs:
        print(job.id, job.job_name, job.status, job.creation_time)

    job_0 = hapi.get_job(job_id=jobs[0].id)
    print(job_0.id, job_0.job_name, job_0.status, job_0.creation_time)

secret = hapi.create_secret(secret_name="sodkamus", secret_value="duh")
print(f"Secret created ({secret})")
