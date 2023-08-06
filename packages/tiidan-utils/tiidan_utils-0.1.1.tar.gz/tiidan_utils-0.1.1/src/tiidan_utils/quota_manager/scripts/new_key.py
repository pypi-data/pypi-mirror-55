from uuid import uuid4
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...crypto import base36encode, sha256_base64
from ..models import *


@click.command()
@click.argument("cid", type=click.STRING, nargs=1)
@click.argument("url", type=click.STRING, nargs=1)
def new(cid, url):
    engine = create_engine(url)
    Session = sessionmaker(engine)
    session = Session()
    api_key = base36encode(uuid4().int)
    print("new api key:", api_key)
    api_hash = sha256_base64(api_key)
    print("hash:", api_hash)
    try:
        session.add(ApiKey(API_HASH=api_hash, COMPANY_ID=cid))
        if not session.query(Quota).get(cid):
            session.add(Quota(COMPANY_ID=cid, QUOTA=5))
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
