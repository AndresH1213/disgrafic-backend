import json
import boto3
import os
from lib.shared.response import send_response
from lib.models.Calculator import Calculator


s3 = boto3.client('s3')


def handler(event, context):
    form = json.loads(event['body'])
    calculator = Calculator(**form)
    total_price = calculator.get_total_price()

    response = {
        "total": f"{total_price:,.2f}",
        "hola": "mundo"  # tiene un watcher :')
    }
    return send_response(json.dumps(response), 200)
