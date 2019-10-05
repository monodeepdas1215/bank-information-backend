from flask import Blueprint, request, jsonify, abort

from app import redis_keys
from app.services.auth_services import authenticated_access
from app.services.composite_services import bank_branches_in_city_service, bank_details_service
from app.services.db_services import get_paginated_results
from app.utils import logger

api = Blueprint('banks_api', __name__, url_prefix='/api')


@api.route('/', methods=["GET"])
def get_all_available_apis():
    return jsonify({
        '/api/banks/': 'search bank branches by ifsc code',
        '/api/banks/branches/': 'search bank branches by name of bank and city'
    }), 200


@api.route('/banks/', methods=['GET'])
@authenticated_access
def get_banks():

    try:
        ifsc = request.args.get('ifsc')

        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        # get the entire results
        banks = bank_details_service(ifsc)

        # paginate and display
        results = get_paginated_results(banks, request.base_url, int(offset), int(limit))

        logger.info("redis keys:", redis_keys())

        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/banks/branches/', methods=['GET'])
@authenticated_access
def get_branches_details():
    try:
        bank_name = request.args.get('bank_name')
        city = request.args.get('city')

        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        # get the entire results
        branches = bank_branches_in_city_service(bank_name, city)

        logger.info("redis keys:", redis_keys())

        # paginate and display
        results = get_paginated_results(branches, request.base_url, int(offset), int(limit))
        return jsonify(results), 200

    except Exception as e:
        logger.exception(e)
        abort(500)