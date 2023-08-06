import json

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from tiidan_utils.sql_handler import SqlHandler


@pytest.fixture
def sql():
    with open("secrets/db_local.json") as f:
        config = json.load(f)
    engine = create_engine(
        URL(
            **{
                "drivername": config.get("drivername", "mysql+pymysql"),
                "username": config["username"],
                "password": config["password"],
                "database": config.get("dbname", config.get("database")),
                "host": config["host"],
                "port": config.get("port", 3306),
            }
        )
    )
    return SqlHandler(engine=engine)


@pytest.fixture
def db_context(sql):
    sql.raw(
        """
    create table test_insert_table
    (
        id int not null,
        name VARCHAR(256) null,
        animal VARCHAR(256) null,
        money int null,
        constraint test_insert_update_pk
            primary key (id)
    );
    """
    )
    sql.raw(
        """
    INSERT INTO test_insert_table (id, name, animal, money)
    VALUES (0, 'tom', 'cat', 100), (1, 'maya', 'dog', 200), (2, 'larry', 'snake', 300)
    """
    )
    yield
    sql.raw(
        """
        DROP TABLE test_insert_table
        """
    )


def test_insert_update(db_context, sql):
    records = [(1, "tom", "elephant")]
    sql.batch_insert_update(
        "test_insert_table", ("id", "name", "animal"), records, ["animal"]
    )
    animal = sql.first("SELECT animal from test_insert_table where id=1")
    assert animal == "elephant"

    records = [(0, "tom", "mouse", 20000)]
    sql.batch_insert_update(
        "test_insert_table", ("id", "name", "animal", "money"), records, ["money"]
    )
    animal = sql.first("SELECT animal from test_insert_table where id=0")
    money = sql.first("SELECT money from test_insert_table where id=0")
    assert animal == "cat"
    assert money == 20000

    records = [(0, "tom", "mouse", 20000), (3, "jerry", "giraffe", -100)]
    sql.batch_insert_update(
        "test_insert_table",
        ("id", "name", "animal", "money"),
        records,
        ["money", "animal"],
    )
    jerry = sql.first("SELECT name from test_insert_table where id=3")
    assert jerry == "jerry"


def test_df(db_context, sql: SqlHandler):
    res = sql.df("select animal from test_insert_table")
    assert isinstance(res, pd.DataFrame)
    assert len(res) == 3
    assert "cat" in res.animal.tolist()
    res = sql.df("select animal from test_insert_table where animal != %s", params=["cat"])
    assert "cat" not in res.animal.tolist()


def test_list(db_context, sql: SqlHandler):
    res = sql.list("select animal from test_insert_table")
    assert isinstance(res, list)
    assert len(res) == 3
    assert "cat" in res
    res = sql.list("select animal from test_insert_table where animal != %s", "cat")
    assert "cat" not in res
