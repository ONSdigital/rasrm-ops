import requests
from flask import Blueprint, render_template, request, current_app as app, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers.collection_exercise_controller import get_collection_exercise
from app.views.survey import get_survey
from app.views.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('collection_exercise_events', __name__, template_folder='templates')

event_keys = ["mps", "go_live", "ref_period_start", "ref_period_end", "return_by", "reminder", "reminder2",
              "reminder3", "employment", "exercise_end"]


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/event', methods=["GET"])
@auth.login_required
def get_collection_exercise_event(survey_id, collection_exercise_id):
    survey = get_survey(survey_id)
    collection_exercise = get_collection_exercise(collection_exercise_id)
    return render_template('collection_exercise_events.html',
                           events=event_keys, collection_exercise=collection_exercise, survey_id=survey_id,
                           collection_exercise_id=collection_exercise_id, survey=survey)


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/event', methods=['POST'])
@auth.login_required
def create_collection_exercise(survey_id, collection_exercise_id):
    if request.form['event'] not in event_keys:
        abort(400)
    timestamp = request.form['event_date']
    try:
        timestamp = convert_to_iso_timestamp(request.form['event_date'])
    except ValueError:
        abort(400)

    event = {
        "tag": request.form['event'],
        "timestamp": timestamp,
    }
    response = requests.post(
        f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexercises/{collection_exercise_id}/events",
        auth=app.config['BASIC_AUTH'], json=event)
    if response.status_code == 409:
        abort(409)
    response.raise_for_status()
    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))
