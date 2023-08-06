import json
import logging
from copy import copy
from functools import wraps
from typing import Callable
from tiidan_utils.aws_utils import add_to_queue

log = logging.getLogger(__name__)


def send_to_next(results, next_tasks):
    if not isinstance(results, list):
        results = [results]
    for task in next_tasks:
        for result in results:
            log.info(f"sending to {task}:" + str(result))
            add_to_queue(task, result)


def sqs_handler(batch=False):
    func = None
    if callable(batch):
        func = copy(batch)
        batch = False

    def wrapper(handler):
        @wraps(handler)
        def _handler(event, context):
            if not event.get("Records"):
                log.info("invoking as lambda with event: " + str(event))
                return handler(event, context)

            if batch:
                records = [json.loads(record["body"]) for record in event["Records"]]
                log.info("invoking as batch: " + str(records))
                handler({"records": records}, context)
            else:
                log.info("invoking sqs handler one by one")
                for record in event["Records"]:
                    body = json.loads(record["body"])
                    log.info("processing record: " + str(body))
                    handler(body, context)

        return _handler

    if callable(func):
        return wrapper(func)
    return wrapper


def s3_handler(func: Callable[[str, str], object]):
    """
    :param func: receives (bucket, key) as arguments
    :return:
    """

    def handler(event, context):
        for record in event["Records"]:
            return func(record["s3"]["bucket"]["name"], record["s3"]["object"]["key"])

    return handler
