import click
from hyperplane_definitions.secret_consts import (
    TOOLS_AND_SERVICES_CATEGORY,
    DATA_SOURCES_AND_TARGETS_CATEGORY,
    DEFAULT_CATEGORY,
)
from tons_cli.common import sdk


SECRET_CATEGORY_CHOICE = [
    TOOLS_AND_SERVICES_CATEGORY,
    DATA_SOURCES_AND_TARGETS_CATEGORY,
]


@click.group()
def secret():
    pass


@secret.command()
@click.option('--name', '-n', help='Secret name', required=True)
@click.option('--value', '-v', help='Secret value', required=True)
@click.option('--category', '-c', help='Secret name to save', default=DEFAULT_CATEGORY, type=click.Choice(SECRET_CATEGORY_CHOICE))
def create(name: str, value: str, category : str):
    '''Create new user secret'''
    result = sdk().create_secret(name, value, category)
    if result:
        click.echo(f"Created secret: {name}")
    else:
        click.echo(f"Failed to create secret: {name}", err=True)


@secret.command("list")
def list_():
    '''List all user secrets'''
    secret_infos = sdk().list_secrets()
    if not isinstance(secret_infos, list):
        click.echo(f"Can't list secrets. Reason: {secret_infos}", err=True)
    else:
        if len(secret_infos) == 0:
            click.echo("No secrets found")
        for secret_info in secret_infos:
            secret_category = secret_info.get("secret_category")
            secret_name = secret_info.get("secret_name")
            click.echo(f"{secret_category}:{secret_name}")

