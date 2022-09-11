import click
from tons_cli.job_group import job
from tons_cli.secret_group import secret
from tons_cli.token_group import token


@click.group()
def cli():
    pass


cli.add_command(job)
cli.add_command(token)
cli.add_command(secret)


def main():
    cli(prog_name='tons')


if __name__ == "__main__":
    main()