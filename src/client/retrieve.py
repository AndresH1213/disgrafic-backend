import json

from pynamodb.exceptions import DoesNotExist
from lib.models.Client import ClientModel


def handler(event, context):
    try:
        found_client = ClientModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Client was not found'})}

    return {'statusCode': 200,
            'body': json.dumps(dict(found_client))}
