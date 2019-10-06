from app.data.data_access_layer import get_banks, get_branch_details, get_branches_by_name_city


def get_all_banks_service():
    return get_banks()


def get_bank_details_service(ifsc_code):
    return get_branch_details(ifsc_code)


def get_all_branches_details_service(name, city):
    return get_branches_by_name_city(name, city)
