import json
import os

import cfenv

cf_env = cfenv.AppEnv()


def env_path(environment):
    if environment == 'prod':
        return ''
    return f"-{environment}"


def get_space():
    vcap = os.getenv('VCAP_APPLICATION')
    return json.loads(vcap).get('space_name')


class Config:
    SERVICE_DOMAIN_SUFFIX = os.getenv("SERVICE_DOMAIN_SUFFIX")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    BASIC_AUTH = (USERNAME, PASSWORD)

    if cf_env.app:
        ENVIRONMENT = get_space()

        ACTION_SERVICE = f"http://actionsvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_EXERCISE_SERVICE = f"http://collectionexercisesvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_INSTRUMENT_SERVICE = f"http://ras-collection-instrument{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
        SAMPLE_SERVICE = f"http://samplesvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
        SURVEY_SERVICE = f"http://surveysvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"


class CIConfig(Config):
    if cf_env.app:
        ENVIRONMENT = get_space()
        ACTION_SERVICE = f"http://rm-action-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_EXERCISE_SERVICE = f"http://rm-collection-exercise-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_INSTRUMENT_SERVICE = f"http://ras-collection-instrument-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        SAMPLE_SERVICE = f"http://rm-sample-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        SURVEY_SERVICE = f"http://rm-survey-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"


class DevConfig(Config):
    USERNAME = "admin"
    PASSWORD = "secret"
    BASIC_AUTH = ("admin", "secret")
    ACTION_SERVICE = 'http://localhost:8151'
    COLLECTION_EXERCISE_SERVICE = 'http://localhost:8145'
    COLLECTION_INSTRUMENT_SERVICE = 'http://localhost:8002'
    SAMPLE_SERVICE = 'http://localhost:8125'
    SURVEY_SERVICE = 'http://localhost:8080'