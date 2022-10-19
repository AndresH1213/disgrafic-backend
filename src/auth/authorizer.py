import boto3

SSM = boto3.client('ssm')


def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource

                }
            ]
        }
    }


def handler(event, *args, **kwargs):
    headers = event['headers']
    if 'authorization' not in headers:
        raise Exception("Unauthorized")
    try:
        response_authorized = generate_policy(
            'admin', 'Allow', event['routeArn']
        )
        token = SSM.get_parameter(
            Name='disgrafic_private_token', WithDecryption=True
        )['Parameter']["Value"]
        if headers['authorization'] == f'Bearer {token}':
            return response_authorized
        else:
            raise Exception('Unauthorized')
    except Exception as e:
        print('Error', e)
