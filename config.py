import os


def env_path(environment):
    if environment == 'prod':
        return ''
    return f"-{environment}"


class Config:
    SERVICE_DOMAIN_SUFFIX = os.getenv("SERVICE_DOMAIN_SUFFIX")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    BASIC_AUTH = (USERNAME, PASSWORD)
    ENVIRONMENT = os.getenv("SPACE")

    ACTION_SERVICE = f"http://actionsvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
    COLLECTION_EXERCISE_SERVICE = f"http://collectionexercisesvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
    COLLECTION_INSTRUMENT_SERVICE = f"http://ras-collection-instrument{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
    SAMPLE_SERVICE = f"http://samplesvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"
    SURVEY_SERVICE = f"http://surveysvc{env_path(ENVIRONMENT)}.{SERVICE_DOMAIN_SUFFIX}"


class CIConfig(Config):
    SERVICE_DOMAIN_SUFFIX = os.getenv("SERVICE_DOMAIN_SUFFIX")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    BASIC_AUTH = (USERNAME, PASSWORD)
    ENVIRONMENT = os.getenv("SPACE")

    ACTION_SERVICE = f"http://rm-action-exercise-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
    COLLECTION_EXERCISE_SERVICE = f"http://rm-collection-exercise-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
    COLLECTION_INSTRUMENT_SERVICE = f"http://ras-collection-insrument-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
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
