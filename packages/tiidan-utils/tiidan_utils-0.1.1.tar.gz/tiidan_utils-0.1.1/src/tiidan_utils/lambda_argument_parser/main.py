import json
import logging

log = logging.getLogger(__name__)


class ErrorResponse(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class Attribute:
    def __init__(self, name, required=False, body=True, query=False):
        self.name = name
        self.required = required
        if not body ^ query:
            raise ValueError("body or query must be exclusively true")
        self.body = body
        self.query = query


class BodyAttribute(Attribute):
    def __init__(self, name, required=False):
        super().__init__(name, required, body=True)


class QueryParameter(Attribute):
    def __init__(self, name, required=False):
        super().__init__(name, required, body=False, query=True)


class ParameterParser:
    def __init__(self, *attributes):
        self.attributes = []
        for attr in attributes:
            if not isinstance(attr, Attribute):
                raise TypeError("{} is not subtype of Attribute".format(attr.name))
        for attr in attributes:
            self.attributes.append(attr)

    def extract(self, body=None, query_params=None):
        if query_params is None:
            query_params = {}
        if body is None:
            body = {}
        args = []
        for attr in self.attributes:
            if attr.body:
                arg = body.get(attr.name)
            elif attr.query:
                arg = query_params.get(attr.name)
            else:
                arg = None
            if arg is None and attr.required:
                raise KeyError(attr.name)
            args.append(arg)
        logged = ", ".join(
            "{}={}".format(attr.name, val) for attr, val in zip(self.attributes, args)
        )
        log.info("received params: {}".format(logged))
        return args
