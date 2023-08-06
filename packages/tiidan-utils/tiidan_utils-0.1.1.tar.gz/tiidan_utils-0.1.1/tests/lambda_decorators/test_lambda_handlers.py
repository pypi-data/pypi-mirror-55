import json
import pytest

from tiidan_utils.lamda_decorators.handlers import sqs_handler

lambda_event = {"key": "value"}
sqs_event = {"Records": [{"body": json.dumps({"key": "value"})}]}


def handler(event, context=None):
    return event["key"]


@pytest.mark.parametrize("event", [lambda_event, sqs_event])
def test_sqs_handler(event):
    return sqs_handler(handler)(event, None)
