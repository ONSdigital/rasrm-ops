import requests
from flask import Blueprint, render_template, url_for, current_app as app, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers.action_controller import get_action_plans, plan_for_collection_exercise, get_action_rules
from app.controllers.collection_exercise_controller import get_collection_exercise
from app.views.survey import get_survey
from app.views.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('action_plan', __name__, template_folder='templates')

# Get this from an endpoint (That doesn't exist yet)
action_types = [
    "SOCIALNOT",
    "SOCIALREM",
    "SOCIALSNE",
    "SOCIALPRENOT",
    "SOCIALICF"
]


@auth.login_required
@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/actions', methods=["GET"])
def get_action_plan(survey_id, collection_exercise_id):
    action_plans = get_action_plans()
    collex_action_plans = [plan for plan in action_plans
                           if plan_for_collection_exercise(plan, collection_exercise_id)]
    action_plan_data = build_combined_action_data(collex_action_plans)

    collection_exercise = get_collection_exercise(collection_exercise_id)
    survey = get_survey(survey_id)
    return render_template('action.html', action_plan_data=action_plan_data, action_types=action_types,
                           collection_exercise=collection_exercise, survey=survey)


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/actions', methods=["POST"])
def create_action_plan(survey_id, collection_exercise_id):
    try:
        timestamp = convert_to_iso_timestamp(request.form['timestamp'])
    except ValueError:
        abort(400)
    rule = {
        'actionPlanId': request.form['action_plan_id'],
        'actionTypeName': request.form['action_rule_type'],
        'name': request.form['name'],
        'description': request.form['description'],
        'triggerDateTime': timestamp,
        'priority': request.form['priority']
    }
    response = requests.post(f'{app.config["ACTION_SERVICE"]}/actionrules',
                             auth=app.config["BASIC_AUTH"], json=rule)
    response.raise_for_status()
    return redirect(url_for('collection_exercise.load_collection_exercise', survey_id=survey_id,
                            collection_exercise_id=collection_exercise_id))


def build_combined_action_data(action_plans):
    action_data = []
    for action_plan in action_plans:
        action_rule_id = action_plan.get('id')
        action_rules = get_action_rules(action_rule_id)
        action_rules = sorted(action_rules, key=lambda k: k['triggerDateTime'])
        action_plan['action_rules'] = action_rules
        action_data.append(action_plan)
    return action_data
