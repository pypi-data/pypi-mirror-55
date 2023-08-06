import os
import re
from datetime import datetime, date
from functools import wraps


def now_string():
    return datetime.now().isoformat().split(".")[0].replace(":", "").replace("-", "")


def remove_symbols_from_supplier(string):
    string = re.sub(r"[^a-zA-Z0-9&]", " ", string)
    string = re.sub(r"\s+", " ", string)
    string = string.strip()
    string = string.lower()
    return string


def camel_case_to_snake_case(str):
    return re.sub(r"(?<=[a-z])[A-Z]|[A-Z](?=[^A-Z])", r"_\g<0>", str).lower().strip("_")


def log_function(logger):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            logger.debug("args: " + str(args))
            logger.debug("kwargs: " + str(kwargs))
            res = func(*args, **kwargs)
            logger.debug("result: " + str(res))
            return res

        return inner

    return wrapper


def json_date_converter(o):
    if isinstance(o, (date, datetime)):
        return o.isoformat()


def local_load_dotenv():
    if os.getenv("ENV") == "LOCAL":
        from dotenv import load_dotenv

        load_dotenv(os.path.join(os.getcwd(), ".env"))


def null_on_error(return_value):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                raise

        return inner

    if callable(return_value):
        return null_on_error(None)(return_value)
    return wrapper
