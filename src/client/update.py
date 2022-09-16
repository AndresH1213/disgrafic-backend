import json
import logging

from pynamodb.exceptions import DoesNotExist
from lib.models.Client import ClientModel


def handler(event, context):
    data = event['body']

    if 'text' not in data and 'checked' not in data:
        logging.error('Validation Failed %s', data)
        return {'statusCode': 422,
                'body': json.dumps({'error_message': 'Couldn\'t update the product.'})}

    try:
        found_client = ClientModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Client was not found'})}

    client_changed = False
    if 'name' in data and data['name'] != found_client.name:
        found_client.name = data['name']
        client_changed = True
    if 'email' in data and data['email'] != found_client.email:
        found_client.email = data['email']
        client_changed = True

    if client_changed:
        found_client.save()
    else:
        logging.info('Nothing changed did not update')

    return {'statusCode': 200,
            'body': json.dumps(dict(found_client))}
