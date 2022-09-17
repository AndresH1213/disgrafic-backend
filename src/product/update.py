import json
import logging

from pynamodb.exceptions import DoesNotExist
from lib.models.Product import ProductModel
from lib.shared.response import send_response


def handler(event, context):
    product_id = event['pathParameters']['id']
    data = json.loads(event['body'])

    try:
        found_product = ProductModel.get(hash_key=product_id)
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Product was not found'})}

    product_changed = False
    if 'name' in data and data['name'] != found_product.name:
        found_product.name = data['name']
        product_changed = True
    if 'price' in data and data['price'] != found_product.price:
        found_product.price = data['price']
        product_changed = True
    if 'label' in data and data['label'] != found_product.label:
        found_product.label = data['label']
        product_changed = True

    if product_changed:
        found_product.save()
    else:
        logging.info('Nothing changed did not update')

    return send_response(json.dumps(dict(found_product)), 200)
