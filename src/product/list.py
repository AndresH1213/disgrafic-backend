import json
from lib.models.Product import ProductModel


def handler(event, context):
    results = ProductModel.scan()

    return {'statusCode': 200,
            'body': json.dumps({'items': [dict(result) for result in results]})}
