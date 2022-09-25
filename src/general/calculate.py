import json
import boto3
import os
from lib.shared.response import send_response


s3 = boto3.client('s3')


def handler(event, context):
    print(event)
    return send_response(json.dumps(event), 200)
