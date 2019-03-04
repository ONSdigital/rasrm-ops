from flask import Blueprint, render_template

from app.auth import auth
from app.controllers.collection_exercise_controller import get_collection_exercise, get_collection_exercise_events
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
