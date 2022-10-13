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

    [product_changed, update_product] = ProductModel.has_product_changed(
        data, found_product)

    if product_changed:
        update_product.save()
    else:
        logging.info('Nothing changed did not update')

    return send_response(json.dumps(dict(update_product)), 200)
