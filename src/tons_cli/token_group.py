import click
from tons_cli.common import get_token, read_config, write_config


@click.group()
def token():
    pass


@token.command()
def get():
    '''Prints token'''
    click.echo(get_token())


@token.command()
# @click.option("--token", help='token value', prompt='Enter Token')
@click.argument("token", nargs=1, required=False)
def set(token: str):
    '''Save token to system'''
    if not token:
        token = click.prompt('Enter Token (Leave empty to cancel action)', default="", show_default=False)
        token = token.strip()
    if not token:
        click.echo("Token not saved")
    else:
        conf = read_config()
        conf.set('DEFAULT', 'sdk_token', token)
        if write_config(conf):
            click.echo("Token saved!")

