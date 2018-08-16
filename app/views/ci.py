import json

import requests
from flask import render_template, Blueprint, url_for, request, current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

blueprint = Blueprint('ci', __name__, template_folder='templates')


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/ci', methods=["GET"])
def get_ci(survey_id, collection_exercise_id):
    classifiers = get_ci_classifiers(survey_id)
    if 'COLLECTION_EXERCISE' in classifiers:
        classifiers['COLLECTION_EXERCISE'] = collection_exercise_id
    return render_template('ci.html', ci_classifiers=classifiers)


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/ci', methods=["POST"])
def create_ci(survey_id, collection_exercise_id):
    ci_classifiers = {k.lower(): v for k, v in request.form.items() if k != 'ci_upload'}
    for value in ci_classifiers.values():
        if not value:
            abort(400)
    upload_eq_ci(survey_id, ci_classifiers)
    link_cis(collection_exercise_id)
    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))


def get_ci_classifier(survey_id, classifier_id):
    response = requests.get(
        url=f'{app.config["SURVEY_SERVICE"]}/surveys/{survey_id}/classifiertypeselectors/{classifier_id}',
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()


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
    return classifiers


def upload_eq_ci(survey_id, ci_classifiers):
    classifiers = {'survey_id': survey_id,
                   'classifiers': json.dumps(ci_classifiers)}
    response = requests.post(
        f"{app.config['COLLECTION_INSTRUMENT_SERVICE']}/collection-instrument-api/1.0.2/upload",
        auth=app.config['BASIC_AUTH'], params=classifiers)
    response.raise_for_status()


def link_cis(collection_exercise_id):
    ci_ids = get_collection_instrument_ids(collection_exercise_id)
    for ci_id in ci_ids:
        link_response = requests.post(
            url=f"{app.config['COLLECTION_INSTRUMENT_SERVICE']}/collection-instrument-api/1.0.2/link-exercise/"
                f"{ci_id}/{collection_exercise_id}",
            auth=app.config['BASIC_AUTH'])
        link_response.raise_for_status()


def get_collection_instrument_ids(collection_exercise_id):
    response = requests.get(
        f'{app.config["COLLECTION_INSTRUMENT_SERVICE"]}/collection-instrument-api/1.0.2/collectioninstrument?'
        f'searchString={{"collection_exercise":"{collection_exercise_id}"}}',
        auth=app.config["BASIC_AUTH"])
    response.raise_for_status()
    return [collection_instrument['id'] for collection_instrument in response.json()]
