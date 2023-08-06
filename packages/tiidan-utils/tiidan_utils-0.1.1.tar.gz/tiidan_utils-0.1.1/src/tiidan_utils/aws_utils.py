import base64
import json
import os
import pickle
from uuid import uuid4
import boto3
from boto3 import client, resource
from botocore.exceptions import ClientError
from .util import json_date_converter

_BUCKET_NAME = os.getenv("BUCKET_NAME")


def translate(text, source="zh", dest="en"):
    translate_client = client(service_name="translate")
    result = translate_client.translate_text(
        Text=text, SourceLanguageCode=source, TargetLanguageCode=dest
    )
    return result.get("TranslatedText")


def get_secret(secret_id: str):
    secrets_manager = client("secretsmanager")
    get_secret_value_response = secrets_manager.get_secret_value(SecretId=secret_id)
    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
    else:
        secret = base64.b64decode(get_secret_value_response["SecretBinary"])
    return json.loads(secret)


def s3_copy(from_, to):
    s3 = resource("s3")
    copy_source = {"Bucket": _BUCKET_NAME, "Key": from_}
    bucket = s3.Bucket(_BUCKET_NAME)
    obj = bucket.Object(to)
    obj.copy(copy_source)


def s3_dump(obj, key, to_pickle=True):
    if to_pickle:
        upload_obj = pickle.dumps(obj)
    else:
        upload_obj = obj
    resource("s3").Object(_BUCKET_NAME, key).put(Body=upload_obj)


def s3_load(key, from_pickle=True):
    response = resource("s3").Object(_BUCKET_NAME, key).get()
    if from_pickle:
        return pickle.loads(response["Body"].read())
    else:
        return response["Body"].read()


def s3_exists(key):
    try:
        resource("s3").Object(_BUCKET_NAME, key).load()
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise


def get_ssm_parameter(key):
    raise Exception("please activate")


def invoke_lambda(function_name, params=None, **kwargs):
    if params is None:
        params = {}
    lambda_client = client("lambda")
    res = lambda_client.invoke(
        FunctionName=function_name, Payload=json.dumps(kwargs), **params
    )["Payload"].read()
    try:
        return json.loads(res)
    except ValueError:
        return res


def add_to_queue(queue_url, body):
    msg = (
        resource("sqs")
        .Queue(queue_url)
        .send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(body),
            MessageAttributes={
                "Recipient": {
                    "StringValue": queue_url.split("/")[-1],
                    "DataType": "String",
                }
            },
        )
    )
    return msg


def send_batch_to_queue(queue_url, bodies):
    if len(bodies) > 10:
        raise Exception("Can't send more than 10 entries at once!")
    entries = [
        {
            "Id": str(uuid4()),
            "MessageBody": json.dumps(body, default=json_date_converter),
            "MessageAttributes": {
                "Recipient": {
                    "StringValue": queue_url.split("/")[-1],
                    "DataType": "String",
                }
            },
        }
        for body in bodies
    ]
    msg = boto3.resource("sqs").Queue(queue_url).send_messages(Entries=entries)
    if msg["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(msg)
    return msg


def s3_delete(key):
    resource("s3").Object(_BUCKET_NAME, key).delete()


def publish_to_sns(arn, **kwargs):
    return resource("sns").Topic(arn).publish(**kwargs)
