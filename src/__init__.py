from flask import Flask

from src.rest.banks_api import api as banks_api
from src.rest.auth_api import api as auth_api
from src.utils.config_access import app_config

app = Flask(__name__)

# updating app config
app.config.update(app_config)

# registering the blueprints
app.register_blueprint(banks_api)
app.register_blueprint(auth_api)