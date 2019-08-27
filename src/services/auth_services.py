import datetime
import traceback

import bcrypt
import jwt as jwt
from flask import request
from functools import wraps

from src.data.data_access_layer import create_user, get_user_credentials
from src.utils.config_access import app_config


def authenticate_user(username: str, password: str):
    # getting user credentials from DB
    user_credentials = get_user_credentials(username)

    # converting password back to bytes for checking
    user_credentials["password"] = user_credentials["password"].encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), user_credentials["password"]):
        return True
    return False


def register_user(username, password):

    print("register user service")

    # creating user in db
    result = create_user(username, encrypt_password(password))

    print(result)

    if not result:
        return {
            "msg": "Unable to create new user. I am sorry !!"
        }

    # generating token
    token = generate_token(username)

    print("token is : ", token)
    return {
        "msg": "Registered",
        "username": username,
        "token": token
    }


def encrypt_password(password):
    # convert it into bytes
    password = str(password).encode("utf-8")
    # generate hash
    return bcrypt.hashpw(password, bcrypt.gensalt())


def verify_token(token):
    try:
        payload = jwt.decode(str(token).encode("utf-8"), app_config['secret_key'])

        result = get_user_credentials(payload["sub"])
        if result:
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
