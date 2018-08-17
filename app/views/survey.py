import requests
from flask import Blueprint, render_template, url_for, current_app as app, request
from werkzeug.utils import redirect

from app.auth import auth

blueprint = Blueprint('survey', __name__, template_folder='templates')


@blueprint.route('/survey/<survey_id>', methods=["GET"])
@auth.login_required
def get_survey_details(survey_id):
    survey = get_survey(survey_id)
    collection_exercises = get_collection_exercises(survey_id)
    return render_template('survey.html', collection_exercises=collection_exercises, survey_id=survey_id, survey=survey)


@blueprint.route('/survey/<survey_id>', methods=['POST'])
@auth.login_required
def create_collection_exercise(survey_id):
    survey = get_survey(survey_id)
    collex = {
        "surveyRef": survey['surveyRef'],
        "name": survey['longName'][:20],
        "exerciseRef": request.form['period'],
        "userDescription": request.form['period_description'],
    }

    response = requests.post(f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexercises",
                             auth=app.config['BASIC_AUTH'], json=collex)
    response.raise_for_status()
    return redirect(url_for('survey.get_survey_details', survey_id=survey_id))


def get_survey(survey_id):
    response = requests.get(f"{app.config['SURVEY_SERVICE']}/surveys/{survey_id}",
                            auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    survey = response.json()
    return survey


def get_collection_exercises(survey):
    response = requests.get(f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexercises/survey/{survey}",
                            auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    collection_exercises = response.json() if response.status_code == 200 else []
    return collection_exercises
