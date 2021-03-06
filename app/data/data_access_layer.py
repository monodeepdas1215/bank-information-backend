import traceback

from pony.orm import db_session, select, commit

from app.data.db_manager import Banks, Branches, Users


@db_session
def get_bank(bank_name):
    bank = select(x for x in Banks if x.name == bank_name)[:]
    if len(bank) == 0:
        return None
    return bank[0].to_dict()


@db_session
def get_banks(bank_id=None):
    if bank_id:
        result = select(x for x in Banks if x.id == bank_id)[:]
    else:
        result = select(x for x in Banks)[:]
    return [i.to_dict() for i in result]


@db_session
def get_bank_branches(bank_id=None):
    if bank_id:
        result = select(x for x in Branches if x.bank_id.id == bank_id)[:]
    else:
        result = select(x for x in Branches)[:]
    return [i.to_dict() for i in result]


@db_session
def get_branches_by_name_city(name, city):
    bank = get_bank(name)
    if not bank:
        return []
    branches = select(x for x in Branches if x.bank_id.id == bank["id"] and x.city == city)[:]
    return [i.to_dict() for i in branches]


@db_session
def get_branch_details(ifsc_code):
    branch = select(x for x in Branches if x.ifsc == ifsc_code)[:]
    if len(branch) == 0:
        return []
    branch = branch[0]
    name = select(x for x in Banks if x.id == branch.bank_id.id)[:][0].name

    branch = branch.to_dict()
    branch.update({"name": name})
    return branch


@db_session
def get_user_credentials(username):
    result = select(x for x in Users if x.username == username)[:]
    if len(result) > 0:
        return result[0].to_dict()
    return None


@db_session
def create_user(username, password: bytes):
    try:
        Users(username=username, password=password.decode("utf-8"))
        commit()
        return True
    except:
        traceback.print_exc()
        return False