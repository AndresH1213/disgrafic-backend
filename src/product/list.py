import json

from lib.models.Product import ProductModel
from lib.shared.response import send_response


def handler(event, context):
    results = ProductModel.scan()
    products = {
        'products': [dict(result) for result in results]
    }

    return send_response(json.dumps(products), 200)
