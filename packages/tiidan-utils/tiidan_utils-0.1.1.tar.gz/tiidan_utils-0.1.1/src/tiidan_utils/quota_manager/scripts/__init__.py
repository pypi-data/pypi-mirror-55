import click
from .new_key import new
from .add_quota import add
from .create_tables import create


@click.group()
def api():
    pass


api.add_command(new)
api.add_command(add)
api.add_command(create)
