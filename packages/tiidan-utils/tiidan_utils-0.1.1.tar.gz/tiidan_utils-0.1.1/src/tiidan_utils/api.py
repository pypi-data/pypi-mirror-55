try:
    from flask import request
except ImportError:
    raise ImportError("Need flask for api utils")

from logging import getLogger
from functools import wraps
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

log = getLogger(__name__)


def load_schema(Schema, from_="body"):
    def decorator(f):
        @wraps(f)
        def inner():
            try:
                if from_ == "query":
                    log.debug(request.args)
                    args = Schema().load(request.args)
                else:
                    log.debug(request.json)
                    args = Schema().load(request.json)
                return f(*args)

            except ValidationError as err:
                log.error(err.messages)
                raise BadRequest(err.messages)

        return inner

    return decorator
