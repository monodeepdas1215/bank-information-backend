from pony.orm import Database, PrimaryKey, Optional, Set, Required

from src.utils.config_access import app_config

db = Database()
print("connecting to DB")
db.bind(provider=app_config['provider'], user=app_config['db_user'],
        password=app_config['db_password'], host=app_config['host'], database=app_config['db'])


print("Defining entities")
class Banks(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    bank_branch = Set('Branches')


class Branches(db.Entity):
    ifsc = PrimaryKey(str)
    bank_id = Required(Banks)
    address = Optional(str)
    city = Optional(str)
    district = Optional(str)
    state = Optional(str)


class Users(db.Entity):
    username = PrimaryKey(str)
    password = Required(str)


print("Generating mappings")
db.generate_mapping(create_tables=True)
print("Mappings generated !!")