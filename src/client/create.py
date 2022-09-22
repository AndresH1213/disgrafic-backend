import json
import logging
import uuid

from lib.models.Client import ClientModel
from lib.shared.response import send_response


def handler(event, context):
    data = json.loads(event['body'])
    isValid = ClientModel.isValid(data)
    if not isValid:
        logging.error('Validation Failed')
        error_response = json.dumps(
            {'error_message': 'Couldn\'t create the client item.'}
        )
        return send_response(error_response, 400)

    new_client = ClientModel(client_id=str(uuid.uuid1()),
                             name=data['name'],
                             phone=data['phone'],
                             email=data['email'],
                             address=data['address'])

    new_client.save()

    return send_response(json.dumps(dict(new_client)), 201)
