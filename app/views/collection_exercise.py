import requests
from flask import Blueprint, render_template, url_for, current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers.collection_exercise_controller import get_collection_exercise_events, get_collection_exercise
from app.views.survey import get_survey

blueprint = Blueprint('collection_exercise', __name__, template_folder='templates')


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>', methods=["GET"])
@auth.login_required
def load_collection_exercise(survey_id, collection_exercise_id):
    survey = get_survey(survey_id)
    collection_exercise = get_collection_exercise(collection_exercise_id)
    events = get_collection_exercise_events(collection_exercise_id)
    executable = collection_exercise['state'] == 'READY_FOR_REVIEW'
    return render_template('collection_exercise.html', survey_id=survey_id,
                           collection_exercise_id=collection_exercise_id, collection_exercise=collection_exercise,
                           events=events, executable=executable, survey=survey)


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>', methods=["POST"])
@auth.login_required
def execute_collection_exercise(survey_id, collection_exercise_id):
    collection_exercise = get_collection_exercise(collection_exercise_id)
    if collection_exercise['state'] != 'READY_FOR_REVIEW':
        abort(400)

    execute_response = requests.post(f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexerciseexecution/"
                                     f"{collection_exercise_id}",
                                     auth=app.config['BASIC_AUTH'])
    execute_response.raise_for_status()
    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))
