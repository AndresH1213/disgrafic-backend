import json
import logging
import uuid

from lib.models.Product import ProductModel
from lib.shared.response import send_response


def handler(event, context):
    data = json.loads(event['body'])

    isValid = ProductModel.isValid(data)
    if not isValid:
        logging.error('Validation Failed')
        error_response = json.dumps(
            {'error_message': 'Couldn\'t create the product item.'}
        )
        return send_response(error_response, 400)

    image_url = data['image_url'] if 'image_url' in data else None

    new_product = ProductModel(product_id=str(uuid.uuid1()),
                               product_type=data['product_type'],
                               subtype=data['subtype'],
                               name=data['name'],
                               price=data['price'],
                               label=data['label'],
                               image_url=image_url)

    new_product.save()

    return send_response(json.dumps(dict(new_product)), 201)
