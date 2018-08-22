from flask import current_app as app
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username == app.config['USERNAME']:
        return app.config['PASSWORD']
