from flask import Blueprint, render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers.action_controller import get_action_plans, plan_for_collection_exercise
from app.sample_loader import SampleLoader
from app.views.ci import get_collection_instrument_ids
from app.views.collection_exercise import get_collection_exercise
from app.views.survey import get_survey

blueprint = Blueprint('sample', __name__, template_folder='templates')


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/sample', methods=["GET"])
@auth.login_required
def get_sample(survey_id, collection_exercise_id):
    collection_exercise = get_collection_exercise(collection_exercise_id)
    survey = get_survey(survey_id)
    return render_template('sample.html', collection_exercise=collection_exercise, survey_id=survey_id,
                           collection_exercise_id=collection_exercise_id, survey=survey)


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/sample', methods=["POST"])
@auth.login_required
def upload_sample(survey_id, collection_exercise_id):
    # TODO: Check if collection exercise valid here too?
    if 'sample' not in request.files:
        abort(400)

    action_plans = get_action_plans()
    action_plan = [plan for plan in action_plans
                   if plan_for_collection_exercise(plan, collection_exercise_id)]
    action_plan_id = action_plan[0]['id']

    # TODO: fail gracefully if instrument not loaded. Log something out and/or render a page with the error
    collection_instrument_id = get_collection_instrument_ids(collection_exercise_id)[0]

    sample_file_in_bytes = request.files['sample'].stream
    sample_file = (line.decode() for line in sample_file_in_bytes)
    sample_loader = SampleLoader()
    sample_loader.load_sample(sample_file, collection_exercise_id, action_plan_id, collection_instrument_id)

    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))
