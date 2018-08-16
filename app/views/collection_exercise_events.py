import requests
from flask import Blueprint, render_template, request, current_app as app, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.views.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('collection_exercise_events', __name__, template_folder='templates')

event_keys = ["mps", "go_live", "ref_period_start", "ref_period_end", "return_by", "reminder", "reminder2",
              "reminder3", "employment", "exercise_end"]


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/event', methods=["GET"])
def get_collection_exercise_event(survey_id, collection_exercise_id):
    return render_template('collection_exercise_events.html',
                           events=event_keys)


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/event', methods=['POST'])
def create_collection_exercise(survey_id, collection_exercise_id):
    if not request.form['event'] or not request.form['event_date']:
        abort(400)
    timestamp = convert_to_iso_timestamp(request.form['event_date'])
    event = {
        "tag": request.form['event'],
        "timestamp": timestamp,
    }
    response = requests.post(
        f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexercises/{collection_exercise_id}/events",
        auth=app.config['BASIC_AUTH'], json=event)
    response.raise_for_status()
    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))

