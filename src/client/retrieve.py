import json

from pynamodb.exceptions import DoesNotExist
from lib.models.Client import ClientModel
from lib.shared.response import send_response


def handler(event, context):
    try:
        found_client = ClientModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        error_response = json.dumps({'error_message': 'Client was not found'})
        return send_response(error_response, 404)

    return send_response(json.dumps(dict(found_client)), 200)
