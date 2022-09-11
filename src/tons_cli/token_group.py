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
@click.option("--token", help='token value', prompt='Enter Token')
def set(token: str):
    '''Save token to system'''
    conf = read_config()
    conf.set('DEFAULT', 'sdk_token', token)
    if write_config(conf):
        click.echo("Token saved!")

