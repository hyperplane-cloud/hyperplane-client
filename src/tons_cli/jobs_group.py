import json
import click
from tons_cli.common import sdk

@click.group()
def jobs():
    pass


@jobs.command()
def all():
    """Get all jobs"""
    jobs = sdk().get_all_jobs()
    if jobs is None:
        click.echo("Failed to get jobs", err=True)
    else:
        click.echo(f"Found {len(jobs)} jobs:")
        for job in jobs:
            click.echo(job)


@jobs.command()
@click.argument('job_id', required=True)
def get(job_id: str):
    """Get a specific job and print its values as a JSON"""
    job = sdk().get_job(job_id)
    if job is None:
        click.echo("Failed to get job", err=True)
    else:
        click.echo(json.dumps(job.job_dict))


@jobs.command()
@click.option('--repo', help="Github repo url", required=True)
@click.option('--instance-type', '-t', help='Instance type to run job on', required=True)
@click.option('--name', 'job_name', help='Job name. Default: "CLI - {repo name}"')
@click.option('--branch', '-b', default='', help='Branch name to clone repo')
@click.option('--config', default='', help='Select hyperplane config in YML. Default is main config')
@click.option('--instance-count', '-c', default=1, help='How many instances to run on', type=int)
def run(
        repo: str,
        instance_type: str,
        job_name: str,
        branch: str,
        config: str,
        instance_count: int,
        ):
    ''' Runs a job on tons ai'''
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


@jobs.command()
@click.argument('job_id', required=True)
def abort(job_id: str):
    """Aborts a job"""
    result = sdk().abort_job(job_id)
    if result:
        click.echo(f"Job {job_id} aborted")
    else:
        click.echo(f"Failed to abort job {job_id}", err=True)
