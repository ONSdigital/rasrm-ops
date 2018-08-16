import os

from flask import Flask
from flask_basicauth import BasicAuth

from app.views import surveys, survey_classifier, survey, collection_exercise_events, setup_blueprints


def create_app(config_name=None):
    app = Flask(__name__, template_folder='templates')
    config_name = config_name or os.getenv("APP_SETTINGS", "Config")
    app_config = f'config.{config_name}'
    app.config.from_object(app_config)
    setup_blueprints(app)
    app.config['BASIC_AUTH_USERNAME'] = app.config['USERNAME']
    app.config['BASIC_AUTH_PASSWORD'] = app.config['PASSWORD']
    app.config['BASIC_AUTH_FORCE'] = True
    BasicAuth(app)
    return app
