from lib.shared.headers import get_default_headers


def send_response(body, status):
    return {
        'headers': get_default_headers(),
        'statusCode': status,
        'body': body
    }
