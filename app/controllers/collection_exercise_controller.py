import requests
from flask import current_app as app


def get_collection_exercise_events(collection_exercise_id):
    response = requests.get(
        f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexercises/{collection_exercise_id}/events",
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()


def get_collection_exercise(collection_exercise_id):
    response = requests.get(
        f"{app.config['COLLECTION_EXERCISE_SERVICE']}/collectionexercises/{collection_exercise_id}",
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()
