import json
import click
from tons_cli.common import sdk


@click.group()
def job():
    pass


@job.command('list')
def list_jobs():
    """List all jobs"""
    jobs = sdk().get_all_jobs()
    if jobs is None:
        click.echo("Failed to get jobs", err=True)
    else:
        if len(jobs) == 0:
            click.echo(f"No jobs found")
        for job in jobs:
            click.echo(job)


@job.command()
@click.argument('job_id', required=True)
def get(job_id: str):
    """Get a specific job and prints it as a JSON"""
    job = sdk().get_job(job_id)
    if job is None:
        click.echo("Failed to get job", err=True)
    else:
        click.echo(json.dumps(job.job_dict))


@job.command()
@click.option('--repo', help="Github repo url", required=True)
@click.option('--instance-type', '-t', help='Instance type to run job on', required=True)
@click.option('--name', 'job_name', help='Job name. Default: "CLI - {repo name}"')
@click.option('--branch', '-b', default='', help='Branch name to clone repo')
@click.option('--config', default='', help='Select hyperplane config in YML. Default is main config')
@click.option('--instance-count', '-c', default=1, help='How many instances to run on', type=int)
def create(
        repo: str,
        instance_type: str,
        job_name: str,
        branch: str,
        config: str,
        instance_count: int,
        ):
    '''Creates a job on tons ai'''
    if not job_name:
        job_name = f"CLI - {repo.split('/')[-1]}"
    response = sdk().create_job(
        git_repo_url=repo,
        job_name=job_name,
        branch_name=branch,
        hyperplane_config=config,
        instance_type=instance_type,
        instance_count=str(instance_count),
    )
    if not response:
        click.echo("Failed to create job", err=True)
    else:
        click.echo(json.dumps(response))


@job.command()
@click.argument('job_id', required=True)
def abort(job_id: str):
    """Aborts a job"""
    result = sdk().abort_job(job_id)
    if result:
        click.echo(f"Job {job_id} aborted")
    else:
        click.echo(f"Failed to abort job {job_id}", err=True)
