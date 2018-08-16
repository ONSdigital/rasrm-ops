import requests
from flask import render_template, Blueprint, url_for, request, current_app as app
from werkzeug.utils import redirect

from app.auth import auth

blueprint = Blueprint('survey_classifier', __name__, template_folder='templates')


@blueprint.route('/survey/<survey_id>/classifiers', methods=["GET"])
@auth.login_required
def get_survey_classifier(survey_id):
    return render_template('survey_classifiers.html',
                           classifier_types=["COLLECTION_INSTRUMENT", "COMMUNICATION_TEMPLATE"],
                           classifiers=["COLLECTION_EXERCISE", "RU_REF", "REGION", "LEGAL_BASIS", "FORM_TYPE",
                                        "SAMPLE_REF", "EQ_ID"])


@blueprint.route('/survey/<survey_id>/classifiers', methods=["POST"])
@auth.login_required
def create_survey_classifier(survey_id):
    classifier_type = request.form['classifier_type']
    classifiers = [classifier for classifier in request.form.values() if classifier != classifier_type]
    classifier = {
        'name': classifier_type,
        'classifierTypes':
            classifiers

    }
    response = requests.post(url=f"{app.config['SURVEY_SERVICE']}/surveys/{survey_id}/classifiers", json=classifier,
                             auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return redirect(url_for('survey.get_survey_details', survey_id=survey_id))
