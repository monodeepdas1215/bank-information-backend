from flask import Flask

from app.app_cache.cache_access_layer import redis_keys
from app.rest.banks_api import api as banks_api
from app.rest.auth_api import api as auth_api
from app.utils import logger
from app.utils.config_access import config

flask_app = Flask(__name__)

# updating app config
flask_app.config.update(config)

# registering the blueprints
flask_app.register_blueprint(banks_api)
flask_app.register_blueprint(auth_api)

logger.info("redis keys:", redis_keys())