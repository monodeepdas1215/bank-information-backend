import datetime
import traceback

import jwt as jwt
from flask import request
from functools import wraps

from src.utils.config_access import app_config


def simple_authentication(auth):

    if auth["username"] == app_config['username'] and auth["password"] == app_config['password']:
        return True
    else:
        return False


def verify_token(token):
    try:
        payload = jwt.decode(str(token).encode("utf-8"), app_config['secret_key'])

        if payload["sub"] == app_config['username']:
            return 1
        return 0
    except jwt.exceptions.DecodeError:
        traceback.print_exc()
        return -1
    except jwt.exceptions.ExpiredSignatureError:
        traceback.print_exc()
        return -2


def authenticated_access(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_token = request.headers.get('Authorization')

        if not authorization_token:
            return {
                       "msg": "Authorization token not present"
            }, 403
        is_verified = verify_token(authorization_token)
        if is_verified == 0:
            return {
                       "msg": "User not authorized"
                   }, 403

        if is_verified == -1:
            return {
                       "msg": "Invalid Token"
                   }, 400

        if is_verified == -2:
            return {
                       "msg": "Token expired"
                   }, 401

        return f(*args, **kwargs)
    return decorated


def generate_token(uname):

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
        'iat': datetime.datetime.utcnow(),
        'sub': uname
    }

    # encode the jwt token
    jwt_token = jwt.encode(payload, app_config['secret_key'], app_config['algorithm'])
    return jwt_token
