from src.data.data_access_layer import get_banks, get_branch_details, get_branches_by_name_city


def get_paginated_results(data, url, start: int, limit: int):

    output = {}
    if len(data) == 0:
        output["result"] = data
        output["next"] = ""
        output["previous"] = ""
        return output

    if not isinstance(data, list):
        data = [data]

    output = {
        "start": start,
        "limit": limit,
        "count": len(data),
    }

    if start + limit > len(data):
        output["next"] = ""
    else:
        output["next"] = "{0}?offset={1}&limit={2}".format(url, start + limit, limit)

    if start - limit < 0:
        output["previous"] = "{0}?offset={1}&limit={2}".format(url, 0, limit)
    elif start > len(data):
        output["previous"] = "{0}?offset={1}&limit={2}".format(url, len(data) - limit, limit)
    else:
        output["previous"] = "{0}?offset={1}&limit={2}".format(url, start - limit, limit)

    output["results"] = data[start:start + limit]

    return output


def get_all_banks_service():
    return get_banks()


def get_bank_details_service(ifsc_code):
    return get_branch_details(ifsc_code)


def get_all_branches_details_service(name, city):
    return get_branches_by_name_city(name, city)
