import json

from pynamodb.exceptions import DoesNotExist
from lib.models.Product import ProductModel


def handler(event, context):
    try:
        found_product = ProductModel.get(hash_key=event['path']['id'])
    except DoesNotExist:
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'Product was not found'})}

    return {'statusCode': 200,
            'body': json.dumps(dict(found_product))}
