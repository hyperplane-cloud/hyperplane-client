import json
from typing import Optional, Tuple
import click

from hyperplane.job import print_pretty_table
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
        job_name = f"CLI - {docker_image}"
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
        
