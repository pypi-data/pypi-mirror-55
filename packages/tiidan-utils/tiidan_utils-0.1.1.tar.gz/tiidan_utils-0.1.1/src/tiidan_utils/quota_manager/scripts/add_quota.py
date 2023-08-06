import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import *


@click.command()
@click.argument("cid", type=click.STRING, nargs=1)
@click.argument("url", type=click.STRING, nargs=1)
@click.argument("n", type=click.INT, nargs=1)
def add(cid, url, n):
    engine = create_engine(url)
    Session = sessionmaker(engine)
    session = Session()
    try:
        quota = session.query(Quota).get(cid)
        quota.QUOTA += n
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
