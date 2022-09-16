import json
from lib.models.Client import ClientModel


def handler(event, context):
    results = ClientModel.scan()

    return {'statusCode': 200,
            'body': json.dumps({'items': [dict(result) for result in results]})}
