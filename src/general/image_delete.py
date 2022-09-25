from lib.models.Image import Image
from lib.shared.response import send_response
import json


def handler(event, context):
    path = event['pathParameters']['path']
    image = Image({"name": path})
    try:
        image.delete_image_s3()
        return send_response("", 204)

    except Exception as e:
        print(e)
        return send_response(json.dumps(e), 500)
