import click
from tons_cli.job_group import job
from tons_cli.secret_group import secret
from tons_cli.token_group import token
from tons_cli.docker_group import docker


@click.group()
def cli():
    pass


cli.add_command(job)
cli.add_command(token)
cli.add_command(secret)
cli.add_command(docker)


def main():
    cli(prog_name='tons')


if __name__ == "__main__":
    main()