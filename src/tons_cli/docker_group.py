import click
import json
from prettytable import PrettyTable
from typing import Optional, List
from urllib import request
from hyperplane.job import Job
from tons_cli.common import sdk



@click.group()
def docker():
    pass


@docker.command(context_settings={"ignore_unknown_options": True})
@click.argument('docker_image', required=True)
@click.argument('docker_params', required=False)
@click.option('--s3-input-path', '-i', required=False)
@click.option('--instance-type', '-t', help='Instance type to run job on', required=True)
@click.option('--name', 'job_name', help='Job name. Default: "cli docker - {docker name}"')
def create(
        docker_image: str,
        s3_input_path: Optional[str],
        instance_type: str,
        job_name: Optional[str],
        docker_params: Optional[str],
        ):
    '''Creates a job to run docker on tons ai'''
    if not docker_params:
        docker_params = ""
    if not job_name:
        job_name = f"docker {docker_image} - {docker_params}"
    response = sdk().create_job(
        job_name=job_name,
        instance_type=instance_type,
        docker_image=docker_image,
        s3_input_path=s3_input_path,
        instance_count=1,
        docker_params=docker_params,
    )
    if not response:
        click.echo("Failed to create job", err=True)
    else:
        click.echo(json.dumps(response, indent=2))


@docker.command('list')
def list_jobs():
    """List all done jobs with s3 path in outputs"""
    jobs = sdk().get_all_jobs()
    if jobs is None:
        click.echo("Failed to get jobs", err=True)
    else:
        if len(jobs) == 0:
            click.echo(f"No jobs found")
        else:
            click.echo(print_image_list(jobs))


@docker.command('download')
@click.argument('job_id', required=True)
def download_images(job_id: str):
    """Download all images of job from s3"""
    job = sdk().get_job(job_id)
    if job is None:
        click.echo("Failed to get job", err=True)
    elif job.status != "Done":
        click.echo("Job is not in Done status")
    elif job.job_dict is None or job.job_dict.get('docker_image') != "custom_app:stable-diffusion":
        click.echo("Job is not from stable-diffusion")
    else:
        outputs = job.job_dict.get('outputs', "").split(";")
        for output in outputs:
            local_file_name = output[0:output.index('?')].split('/')[-1]
            print(f"Downloading to {local_file_name} from {output}")
            response = request.urlretrieve(output, local_file_name)
            print(response)


def print_image_list(jobs: List[Job]) -> str:

    pt = PrettyTable(['Start Time', 'ID', 'Params', 'Output'], align='l',sortby='Start Time')

    for job in jobs:
        job_dict = job.job_dict
        if job.status == "Done" and job_dict and job_dict.get('docker_image') == "custom_app:stable-diffusion":
            outputs = job_dict.get('outputs', "").split(";")
            for output in outputs[2:]:
                pt.add_row([job.start_time, job.id, job_dict.get('docker_params'), output])

    return pt.get_string()
