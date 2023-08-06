import click
from sqlalchemy import create_engine
from ..models import *


@click.command()
@click.argument("url", type=click.STRING, nargs=1)
def create(url):
    engine = create_engine(url)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
