import requests
from flask import Blueprint, render_template, url_for, request, current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

blueprint = Blueprint('sample', __name__, template_folder='templates')


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/sample', methods=["GET"])
def get_sample(survey_id, collection_exercise_id):
    return render_template('sample.html')


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/sample', methods=["POST"])
def upload_sample(survey_id, collection_exercise_id):
    # Check if collection exercise valid?
    if 'sample' not in request.files:
        abort(400)

    sample_summary_id = upload_sample_file(survey_id, request.files['sample'])
    link_sample(collection_exercise_id, sample_summary_id)
    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))


def get_survey_type(survey_id):
    response = requests.get(url=f'{app.config["SURVEY_SERVICE"]}/surveys/{survey_id}',
                            auth=app.config['BASIC_AUTH'])
    response.raise_for_status()

    survey = response.json()
    if survey['surveyType'] == 'Business':
        return 'B'
    elif survey['surveyType'] == 'Social':
        return 'Social'


def upload_sample_file(survey_id, file):
    survey_type = get_survey_type(survey_id)
    response = requests.post(url=f'{app.config["SAMPLE_SERVICE"]}/samples/{survey_type}/fileupload',
                             auth=app.config['BASIC_AUTH'], files={'file': file})
    response.raise_for_status()
    return response.json()['id']


def link_sample(collection_exercise_id, sample_summary_id):
    sample_summaries = {'sampleSummaryIds': [sample_summary_id]}
    response = requests.put(
        url=f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexercises/link/{collection_exercise_id}",
        json=sample_summaries, auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
