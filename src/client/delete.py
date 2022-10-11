import json
from pynamodb.exceptions import DoesNotExist, DeleteError

from lib.models.Client import ClientModel
from lib.shared.response import send_response


def handler(event, context):
    try:
        found_client = ClientModel.get(
            hash_key=event['pathParameters']['id'])
    except DoesNotExist:
        error_response = json.dumps({'error_message': 'Client was not found'})
        return send_response(error_response, 404)
    try:
        found_client.delete()
    except DeleteError:
        error_response = json.dumps(
            {'error_message': 'Unable to delete the client'}
        )
        return send_response(error_response, 400)

    return send_response("", 204)
