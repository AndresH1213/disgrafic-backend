import json
from lib.models.Client import ClientModel
from lib.shared.response import send_response


def handler(event, context):
    results = ClientModel.scan()
    clients = {
        'clients': [dict(result) for result in results]
    }

    return send_response(json.dumps(clients), 200)
