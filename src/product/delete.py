import json

from pynamodb.exceptions import DoesNotExist, DeleteError
from lib.models.Product import ProductModel


def handler(event, context):
    try:
        found_product = ProductModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Product was not found'})}
    try:
        found_product.delete()
    except DeleteError:
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Unable to delete the Product'})}

    return {'statusCode': 204}
