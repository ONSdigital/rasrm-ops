import requests
from flask import render_template, Blueprint, url_for, request, current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.views.survey import get_survey

blueprint = Blueprint('survey_classifier', __name__, template_folder='templates')

classifier_selector_types = ["COLLECTION_INSTRUMENT", "COMMUNICATION_TEMPLATE"]


@blueprint.route('/survey/<survey_id>/classifiers', methods=["GET"])
@auth.login_required
def get_survey_classifier(survey_id):
    survey = get_survey(survey_id)
    return render_template('survey_classifiers.html',
                           classifier_types=classifier_selector_types,
                           classifiers=["COLLECTION_EXERCISE", "RU_REF", "REGION", "LEGAL_BASIS", "SAMPLE_REF"],
                           survey=survey, survey_id=survey_id)


@blueprint.route('/survey/<survey_id>/classifiers', methods=["POST"])
@auth.login_required
def create_survey_classifier(survey_id):
    classifier_type = request.form['classifier_type']
    if classifier_type not in classifier_selector_types:
        abort(400)
    classifiers = build_classifiers(classifier_type)
    if not classifiers.get('classifierTypes'):
        abort(400)
    response = requests.post(url=f"{app.config['SURVEY_SERVICE']}/surveys/{survey_id}/classifiers", json=classifiers,
                             auth=app.config['BASIC_AUTH'])
    if response.status_code == 409:
        abort(409)
    response.raise_for_status()
    return redirect(url_for('survey.get_survey_details', survey_id=survey_id))


def build_classifiers(classifier_type):
    classifiers = [classifier for classifier in request.form.values() if classifier != classifier_type]
    classifier = {
        'name': classifier_type,
        'classifierTypes':
            classifiers

    }
    return classifier
