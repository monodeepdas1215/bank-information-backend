import datetime
import traceback

import bcrypt
import jwt as jwt
from flask import request
from functools import wraps

from app.data.data_access_layer import create_user, get_user_credentials
from app.utils.config_access import config


def authenticate_user(username: str, password: str):
    # getting user credentials from DB
    user_credentials = get_user_credentials(username)

    if not user_credentials:
        return False

    # converting password back to bytes for checking
    user_credentials["password"] = user_credentials["password"].encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), user_credentials["password"]):
        return True
    return False


def register_user(username, password):

    # creating user in db
    result = create_user(username, encrypt_password(password))

    if not result:
        return {
            "msg": "Unable to create new user. I am sorry !!"
        }

    # generating token
    token = generate_token(username)

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
        payload = jwt.decode(str(token).encode("utf-8"), config['SECRET_KEY'])

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

        if config['AUTH'] in ["off", "False", "false", "0"]:
            return f(*args, **kwargs)

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
    jwt_token = jwt.encode(payload, config['SECRET_KEY'], config['ALGORITHM'])
    return jwt_token
