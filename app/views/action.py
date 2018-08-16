import requests
from flask import Blueprint, render_template, url_for, current_app as app, request
from werkzeug.utils import redirect

from app.views.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('action_plan', __name__, template_folder='templates')

# Get this from an endpoint (That doesn't exist yet)
action_types = [
    "BSNOT",
    "BSREM",
    "BSSNE",
    "BSNL",
    "BSNE",
    "BSRL",
    "BSRE",
    "SOCIALNOT",
    "SOCIALREM",
    "SOCIALSNE",
    "SOCIALPRENOT",
]


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/actions', methods=["GET"])
def get_action_plan(survey_id, collection_exercise_id):
    response = requests.get(f'{app.config["ACTION_SERVICE"]}/actionplans',
                            auth=app.config["BASIC_AUTH"])
    response.raise_for_status()
    plans = [plan for plan in response.json() if
             plan_for_collection_exercise(plan, collection_exercise_id)]
    return render_template('action.html', plans=plans, action_types=action_types)


def plan_for_collection_exercise(plan, collection_exercise_id):
    if not plan['selectors']:
        return False
    return plan['selectors']['collectionExerciseId'] == collection_exercise_id


@blueprint.route('/survey/<survey_id>/collection/<collection_exercise_id>/actions', methods=["POST"])
def create_action_plan(survey_id, collection_exercise_id):
    timestamp = convert_to_iso_timestamp(request.form['timestamp'])
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
