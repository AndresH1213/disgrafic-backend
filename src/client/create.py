import json
import logging
import uuid

from lib.models.Client import ClientModel


def handler(event, context):
    data = json.loads(event['body'])
    isValid = ClientModel.isValid(data)
    if not isValid:
        logging.error('Validation Failed')
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Couldn\'t create the client item.'})}

    new_client = ClientModel(client_id=str(uuid.uuid1()),
                             name=data['name'],
                             phone=data['phone'],
                             email=data['email'],
                             address=data['address'])

    new_client.save()

    return {'statusCode': 201,
            'body': json.dumps(dict(new_client))}
