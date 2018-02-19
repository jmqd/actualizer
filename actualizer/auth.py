import boto3
import os
import hmac
import hashlib
import base64

COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.environ.get('COGNITO_CLIENT_SECRET')
cognito = boto3.client('cognito-idp')

def sign_up(username: str, email: str, phone: str, password: str) -> None:
    response = cognito.sign_up(
        ClientId = COGNITO_CLIENT_ID,
        SecretHash = _calculate_secret_hash(username),
        Username = username,
        Password = password,
        UserAttributes = [
            {'Name': 'email', 'Value': email},
            {'Name': 'phone_number', 'Value': phone}
        ]
    )


def confirm_sign_up(username: str, confirmation_code: str) -> None:
    response = cognito.confirm_sign_up(
        ClientId = COGNITO_CLIENT_ID,
        SecretHash = _calculate_secret_hash(username),
        Username = username,
        ConfirmationCode = confirmation_code
    )


def _calculate_secret_hash(username: str) -> str:
    msg = (username + COGNITO_CLIENT_ID).encode('utf-8')
    digest = hmac.new(
        COGNITO_CLIENT_SECRET.encode('utf-8'),
        msg,
        hashlib.sha256
    ).digest()
    secret_hash = base64.b64encode(digest).decode()
    return secret_hash

