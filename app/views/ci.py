import json

import requests
from flask import render_template, Blueprint, url_for, request, current_app as app
from requests import HTTPError
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers.collection_exercise_controller import get_collection_exercise
from app.views.survey import get_survey

blueprint = Blueprint('ci', __name__, template_folder='templates')


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/ci', methods=["GET"])
def get_ci(survey_id, collection_exercise_id):
    classifiers = get_ci_classifiers(survey_id)
    if 'COLLECTION_EXERCISE' in classifiers:
        classifiers['COLLECTION_EXERCISE'] = collection_exercise_id
    if 'EQ_ID' in classifiers:
        classifiers['EQ_ID'] = 'census'
    collection_exercise = get_collection_exercise(collection_exercise_id)
    survey = get_survey(survey_id)
    return render_template('ci.html', ci_classifiers=classifiers, collection_exercise=collection_exercise,
                           survey_id=survey_id, collection_exercise_id=collection_exercise_id, survey=survey)


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/ci', methods=["POST"])
@auth.login_required
def create_ci(survey_id, collection_exercise_id):
    form_classifiers = {k.lower(): v for k, v in request.form.items() if k != 'ci_upload'}
    survey_classifiers = get_ci_classifiers(survey_id)
    for key in survey_classifiers.keys():
        if key.lower() not in form_classifiers or not form_classifiers[key.lower()]:
            abort(400)

    try:
        upload_eq_ci(survey_id, form_classifiers)
        link_cis(collection_exercise_id)
    except HTTPError as e:
        if e.response.status_code == 409:
            abort(409)
        raise
    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))


# TODO: Move to controller
def get_ci_classifier(survey_id, classifier_id):
    response = requests.get(
        url=f'{app.config["SURVEY_SERVICE"]}/surveys/{survey_id}/classifiertypeselectors/{classifier_id}',
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()


# TODO: Move to controller
def get_ci_classifiers(survey_id):
    response = requests.get(url=f'{app.config["SURVEY_SERVICE"]}/surveys/{survey_id}/classifiertypeselectors',
                            auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    if response.status_code == 204:
        classifier_ids = []
    else:
        classifier_ids = [classifier_selector['id'] for classifier_selector in response.json() if
                          classifier_selector['name'] == 'COLLECTION_INSTRUMENT']

    classifiers = {}
    for classifier_id in classifier_ids:
        classifiers_for_id = get_ci_classifier(survey_id, classifier_id)
        for classifier in classifiers_for_id['classifierTypes']:
            classifiers[classifier] = ''
    classifiers['EQ_ID'] = ''
    classifiers['FORM_TYPE'] = ''
    return classifiers


# TODO: Move to controller
def upload_eq_ci(survey_id, ci_classifiers):
    classifiers = {'survey_id': survey_id,
                   'classifiers': json.dumps(ci_classifiers)}
    response = requests.post(
        f"{app.config['COLLECTION_INSTRUMENT_SERVICE']}/collection-instrument-api/1.0.2/upload",
        auth=app.config['BASIC_AUTH'], params=classifiers)
    response.raise_for_status()


# TODO: Move to controller
def link_cis(collection_exercise_id):
    ci_ids = get_collection_instrument_ids(collection_exercise_id)
    for ci_id in ci_ids:
        link_response = requests.post(
            url=f"{app.config['COLLECTION_INSTRUMENT_SERVICE']}/collection-instrument-api/1.0.2/link-exercise/"
                f"{ci_id}/{collection_exercise_id}", auth=app.config['BASIC_AUTH'])
        link_response.raise_for_status()


# TODO: Move to controller
def get_collection_instrument_ids(collection_exercise_id):
    response = requests.get(
        f'{app.config["COLLECTION_INSTRUMENT_SERVICE"]}/collection-instrument-api/1.0.2/collectioninstrument?'
        f'searchString={{"collection_exercise":"{collection_exercise_id}"}}',
        auth=app.config["BASIC_AUTH"])
    response.raise_for_status()
    return [collection_instrument['id'] for collection_instrument in response.json()]
