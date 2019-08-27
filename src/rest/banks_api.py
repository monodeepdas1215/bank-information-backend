import traceback
from flask import Blueprint, request, jsonify, abort

from src.services.auth_services import authenticated_access
from src.services.db_services import get_paginated_results, get_bank_details_service, get_all_branches_details_service

api = Blueprint('banks_api', __name__, url_prefix='/api')


@api.route('/banks/<ifsc>', methods=['GET'])
@authenticated_access
def get_banks(ifsc):

    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 10)

        # get the entire results
        banks = get_bank_details_service(ifsc)

        # paginate and display
        results = get_paginated_results(banks, request.base_url, int(offset), int(limit))

        return jsonify(results), 200

    except Exception:
        traceback.print_exc()
        abort(500)


@api.route('/banks/<bank_name>/branches/<city>', methods=['GET'])
@authenticated_access
def get_branches_details(bank_name, city):
    try:
        # reading the request arguments
        offset = request.args.get('offset', 0)
        limit = request.args.get('limit', 2)

        # get the entire results
        branches = get_all_branches_details_service(bank_name, city)

        # paginate and display
        results = get_paginated_results(branches, request.base_url, int(offset), int(limit))

        return jsonify(results), 200

    except Exception:
        traceback.print_exc()
        abort(500)