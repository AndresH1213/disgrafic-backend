import json
from pynamodb.exceptions import DoesNotExist

from lib.models.Product import ProductModel
from lib.shared.response import send_response


def handler(event, context):
    try:
        found_product = ProductModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        error_response = json.dumps({'error_message': 'Product was not found'})
        return send_response(error_response, 404)

    return send_response(json.dumps(dict(found_product)), 200)
