import boto3
import json
from lib.shared.response import send_response

SSM = boto3.client('ssm')

"""
  caveat, this low level of security is not recommended for large applications with many users,
  consider Cognito, OAuth or Custom Authorizers JWT-validation-based.
"""


def validate_admin_auth(user, password):
    user_parameter = SSM.get_parameter(
        Name="disgrafic_admin_username", WithDecryption=True
    )['Parameter']
    password_parameter = SSM.get_parameter(
        Name="disgrafic_admin_pass", WithDecryption=True
    )['Parameter']
    admin_user, admin_pass = user_parameter["Value"], password_parameter["Value"]

    return user == admin_user and password == admin_pass


def handler(event, context):
    body = json.loads(event['body'])
    if 'user' not in body and 'password' not in body:
        error_response = json.dumps(
            {'error_message': 'User or password are missing.'}
        )
        send_response(error_response, 400)

    valid_credentials = validate_admin_auth(body['user'], body['password'])
    if valid_credentials:
        token = SSM.get_parameter(
            Name='disgrafic_private_token', WithDecryption=True
        )['Parameter']["Value"]
        return send_response(json.dumps({'token': token}), 200)
    else:
        response = json.dumps({"message": "Invalid Credentials"})
        return send_response(response, 401)
