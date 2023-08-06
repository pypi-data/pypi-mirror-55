import click
from ..quota_manager.scripts import api


@click.group()
def cli():
    pass


cli.add_command(api)
