import logging
from tiidan_utils.util import log_function


def test_function_logger():
    @log_function(logging)
    def foo(*args, **kwargs):
        return "hello"

    args = [1, "str"]
    kwargs = {"key": "value"}
    foo(*args, **kwargs)
