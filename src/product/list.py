import json

from lib.models.Product import ProductModel
from lib.shared.response import send_response

ALLOWED_LABEL = ['material', 'mercancia']


def handler(event, context):
    q = 'queryStringParameters'
    query_params = q in event and event[q]

    if query_params and "label" in query_params and query_params['label'] in ALLOWED_LABEL:
        results = list(ProductModel.label_index.query(
            str(query_params['label'])))
    else:
        results = ProductModel.scan()

    products = {
        'products': [dict(result) for result in results]
    }

    return send_response(json.dumps(products), 200)
