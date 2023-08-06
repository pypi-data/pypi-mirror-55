import json
from logging import getLogger

log = getLogger(__name__)


def validate_schema(Schema):
    def wrapper(func):
        schema = Schema()

        def handler(event, context):
            log.debug("received event: " + json.dumps(event))
            args, kwargs = schema.load(event)
            return func(*args, **kwargs, context=context)

        return handler

    return wrapper
