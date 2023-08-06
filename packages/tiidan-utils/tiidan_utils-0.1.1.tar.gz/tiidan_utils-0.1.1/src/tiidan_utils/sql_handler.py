import logging
from contextlib import contextmanager
from warnings import warn

try:
    import pandas as pd
except ImportError:
    warn("pandas not found")
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

@contextmanager
def session_context(Session):
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()


class SqlException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SqlHandler:
    Session = None
    engine = None

    def __init__(self, config=None, engine=None):
        if config is not None:
            self.config(config)
        if engine is not None:
            self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def from_engine(cls, engine):
        return cls(engine=engine)

    def config(self, config):
        log.debug("setting db connection to: {}".format(config["host"]))
        config = {
            "drivername": config.get("drivername", "mysql+pymysql"),
            "username": config["username"],
            "password": config["password"],
            "database": config.get("dbname", config.get("database")),
            "host": config["host"],
            "port": config.get("port", 3306),
        }
        self.engine = create_engine(URL(**config), paramstyle="pyformat")

    def raw(self, query, bindings=None):
        if bindings is None:
            bindings = {}
        with session_context(self.Session) as session:
            res = session.execute(query, bindings)
        res.close()
        return res

    def df(self, query, params=None, **kwargs):
        res = pd.read_sql(query, self.engine, params=params, **kwargs)
        self.engine.dispose()
        return res

    def first(self, query, params=None):
        if params is None:
            params = {}
        return self.engine.scalar(query, params)

    def batch_insert_update(
        self, table, columns, values, update_columns, batch_size=100
    ):
        """
        :param table:
        :param columns:
        :param values:
        :param update_columns:
        :param batch_size:
        :return:
        """
        for row in values:
            if len(row) != len(columns):
                raise KeyError(f"All records need to have all columns'")
        for i in range(0, len(values), batch_size):
            batch = values[i : i + batch_size]
            numbered_dicts = [
                {f"{key}{i}": value for key, value in zip(columns, row)}
                for i, row in enumerate(batch)
            ]
            values_strings = [
                tuple(map(lambda x: ":" + x, d.keys())) for d in numbered_dicts
            ]
            query_values = ",".join(f"({','.join(map(str,v))})" for v in values_strings)
            bindings = {k: v for d in numbered_dicts for k, v in d.items()}
            update = ",".join(f"{col}=VALUES({col})" for col in update_columns)
            query = f"""
            INSERT INTO {table} ({','.join(columns)})
            VALUES {query_values}
            ON DUPLICATE KEY UPDATE {update}
            """
            res = self.raw(query, bindings)
            res.close()

    def list(self, query, *args, **kwargs):
        try:
            cursor = self.engine.execute(query, *args, **kwargs)
        finally:
            self.engine.dispose()
        res_list = [s[0] for s in cursor]
        cursor.close()
        return res_list
