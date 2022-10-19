import boto3
import json
from lib.shared.response import send_response

SSM = boto3.client('ssm')


def handler(event, context):
    q = event['queryStringParameters']
    if 'token' not in q:
        error_response = json.dumps(
            {'error_message': 'There is no token in the request. Unauthorized'}
        )
        send_response(error_response, 401)

    token_db = SSM.get_parameter(
        Name='disgrafic_private_token', WithDecryption=True
    )['Parameter']["Value"]
    if token_db == q['token']:
        return send_response(json.dumps({'ok': True}), 200)
    else:
        response = json.dumps({"message": "Invalid Credentials"})
        return send_response(response, 401)
