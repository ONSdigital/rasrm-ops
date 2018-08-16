import requests
from flask import Blueprint, render_template, url_for, request

from flask import current_app as app
from werkzeug.utils import redirect

from app.auth import auth

blueprint = Blueprint('surveys', __name__, template_folder='templates')


@blueprint.route('/survey', methods=["GET"])
@auth.login_required
def get_survey():
    return render_template('surveys.html', legal_basis=get_legal_basis(), survey_types=["Business", "Social"],
                           surveys=get_surveys())


@blueprint.route('/survey', methods=['POST'])
@auth.login_required
def create_survey():
    survey = {
        'surveyRef': request.form['survey_ref'],
        'shortName': request.form['short_name'],
        'longName': request.form['long_name'],
        'legalBasisRef': request.form['legal_basis'],
        'surveyType': request.form['survey_type']
    }
    response = requests.post(f"{app.config['SURVEY_SERVICE']}/surveys", auth=app.config['BASIC_AUTH'], json=survey)
    response.raise_for_status()
    return redirect(url_for('surveys.get_survey'))


def get_legal_basis():
    response = requests.get(f"{app.config['SURVEY_SERVICE']}/legal-bases", auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    legal_basis = [legal_basis['ref'] for legal_basis in response.json()]
    return legal_basis


def get_surveys():
    response = requests.get(f"{app.config['SURVEY_SERVICE']}/surveys", auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()