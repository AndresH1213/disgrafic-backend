import json
import logging
from turtle import isvisible
import uuid

from lib.models.Product import ProductModel
from lib.shared.response import send_response


def handler(event, context):
    print(event['body'])
    data = json.loads(event['body'])
    isValid = ProductModel.isValid(data)
    if not isValid:
        logging.error('Validation Failed')
        error_response = json.dumps(
            {'error_message': 'Couldn\'t create the product item.'}
        )
        return send_response(error_response, 400)

    new_product = ProductModel(product_id=str(uuid.uuid1()),
                               product_type=data['product_type'],
                               subtype=data['subtype'],
                               name=data['name'],
                               price=data['price'],
                               label=data['label'])

    new_product.save()

    return send_response(json.dumps(dict(new_product)), 201)
