import requests
from flask import current_app as app


def get_action_plans():
    response = requests.get(
        f"{app.config['ACTION_SERVICE']}/actionplans",
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()


def get_action_rules(action_plan_id):
    response = requests.get(
        f"{app.config['ACTION_SERVICE']}/actionrules/actionplan/{action_plan_id}",
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()


def plan_for_collection_exercise(plan, collection_exercise_id):
    if not plan['selectors']:
        return False
    return plan['selectors']['collectionExerciseId'] == collection_exercise_id
