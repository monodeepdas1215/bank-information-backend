from pony.orm import Database, PrimaryKey, Optional, Set, Required

from app.utils import logger
from app.utils.config_access import config

db = Database()
logger.info("connecting to DB")
db.bind(provider=config['PROVIDER'], user=config['DB_USER'],
        password=config['DB_PASSWORD'], host=config['HOST'], database=config['DB'])

logger.info("Defining entities")


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


logger.info("Generating mappings")
db.generate_mapping(create_tables=True)
logger.info("Mappings generated !!")