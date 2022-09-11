import click
from hyperplane_definitions.secret_consts import ALL_CATEGORIES, DEFAULT_CATEGORY
from tons_cli.common import sdk


@click.group()
def secret():
    pass


@secret.command()
@click.option('--name', '-n', help='Secret name', required=True)
@click.option('--value', '-v', help='Secret value', required=True)
@click.option('--category', '-c', help='Secret name to save', default=DEFAULT_CATEGORY, type=click.Choice(ALL_CATEGORIES))
def create(name: str, value: str, category : str):
    result = sdk().create_secret(name, value, category)
    if result:
        click.echo(f"Created secret: {name}")
    else:
        click.echo(f"Failed to create secret: {name}", err=True)

