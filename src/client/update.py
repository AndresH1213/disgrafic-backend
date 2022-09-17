import json
import logging

from pynamodb.exceptions import DoesNotExist
from lib.models.Client import ClientModel
from lib.shared.response import send_response


def handler(event, context):
    data = event['body']

    try:
        found_client = ClientModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        error_response = json.dumps({'error_message': 'Client was not found'})
        return send_response(error_response, 404)

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

    return send_response(json.dumps(dict(found_client)), 200)
