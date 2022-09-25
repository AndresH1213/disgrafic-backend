from lib.models.Image import Image
from lib.shared.response import send_response
import json


def handler(event, context):
    data = event['queryStringParameters']
    image = Image(data)
    image.validate()

    if (len(image.errors) > 0):
        error_response = json.dumps({"errors": image.errors})
        return send_response(error_response, 400)

    try:
        response = image.put_image_s3()

        response_object = {"status": "ok", "response": response}
        return send_response(json.dumps(response_object), 200)

    except Exception as e:
        print(e)
        return send_response(json.dumps(e), 500)
