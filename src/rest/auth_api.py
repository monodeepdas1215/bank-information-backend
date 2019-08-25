import traceback

from flask import Blueprint, request, abort
from src.services.auth_services import simple_authentication, generate_token
from src.utils.json_encoders import jsonify

api = Blueprint('auth_api', __name__, url_prefix='/auth')


@api.route('/login', methods=['GET'])
def login():
    print(request.headers.get('Authorization'))
    try:
        if request.authorization:

            if simple_authentication(request.authorization):
                return jsonify({
                    "token": generate_token(request.authorization["username"])
                }), 200
            else:
                return jsonify({
                    "msg": "The username/password is not wrong/not present."
                }), 403
        else:
            return jsonify({
                "msg": "Username/Password not found in authorization header"
            }), 400
    except Exception:
        traceback.print_exc()
        abort(500)