import json
from sqlalchemy.engine.url import URL


def get_db_url(path):
    with open(path) as json_file:
        db_config = json.load(json_file)

    db_config = {
        "username": db_config["username"],
        "port": db_config.get("port", 3306),
        "database": db_config["dbname"],
        "password": db_config["password"],
        "host": db_config["host"],
    }

    return URL(drivername="mysql+pymysql", **db_config)
