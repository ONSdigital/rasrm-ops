import os

import cfenv

cf_env = cfenv.AppEnv()


def env_path(environment):
    return f"-{environment}"


class Config:
    PORT = os.getenv('PORT')  # This is not used in run.py which isn't used in cloudfoundry
    SERVICE_DOMAIN_SUFFIX = os.getenv("SERVICE_DOMAIN_SUFFIX")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    BASIC_AUTH = (USERNAME, PASSWORD)

    if cf_env.app:
        ENVIRONMENT = cf_env.space
        ACTION_SERVICE = f"http://actionsvc-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_EXERCISE_SERVICE = f"http://collectionexercisesvc-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_INSTRUMENT_SERVICE = f"http://ras-collection-instrument-{ENVIRONMENT}." \
            f"{SERVICE_DOMAIN_SUFFIX}"
        SAMPLE_SERVICE = f"http://samplesvc-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        SURVEY_SERVICE = f"http://surveysvc-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"


class CIConfig(Config):
    SERVICE_DOMAIN_SUFFIX = os.getenv("SERVICE_DOMAIN_SUFFIX")
    if cf_env.app:
        ENVIRONMENT = cf_env.space
        ACTION_SERVICE = f"http://rm-action-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_EXERCISE_SERVICE = f"http://rm-collection-exercise-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        COLLECTION_INSTRUMENT_SERVICE = f"http://ras-collection-instrument-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        SAMPLE_SERVICE = f"http://rm-sample-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"
        SURVEY_SERVICE = f"http://rm-survey-service-{ENVIRONMENT}.{SERVICE_DOMAIN_SUFFIX}"


class K8SDevelopmentConfig(Config):
    PORT = os.getenv("PORT", 80)
    USERNAME = os.getenv('USERNAME', "admin")
    PASSWORD = os.getenv('USERNAME', "secret")
    BASIC_AUTH = ("admin", "secret")
    ACTION_SERVICE = os.getenv('ACTION_SERVICE')
    COLLECTION_EXERCISE_SERVICE = os.getenv('COLLECTION_EXERCISE_SERVICE')
    COLLECTION_INSTRUMENT_SERVICE = os.getenv('COLLECTION_INSTRUMENT_SERVICE')
    SAMPLE_SERVICE = os.getenv('SAMPLE_SERVICE')
    SURVEY_SERVICE = os.getenv('SURVEY_SERVICE')
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'Case.CaseDelivery')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    REDIS_HOST = os.getenv('REDIS_SERVICE_HOST')
    REDIS_PORT = os.getenv('REDIS_SERVICE_PORT')
    REDIS_DB = os.getenv('REDIS_DB')


class DevelopmentConfig(Config):
    PORT = os.getenv("PORT", 8003)
    USERNAME = "admin"
    PASSWORD = "secret"
    BASIC_AUTH = ("admin", "secret")
    ACTION_SERVICE = 'http://localhost:8151'
    COLLECTION_EXERCISE_SERVICE = 'http://localhost:8145'
    COLLECTION_INSTRUMENT_SERVICE = 'http://localhost:8002'
    SAMPLE_SERVICE = 'http://localhost:8125'
    SURVEY_SERVICE = 'http://localhost:8080'
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'Case.CaseDelivery')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    REDIS_HOST = os.getenv('REDIS_SERVICE_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_SERVICE_PORT', '7379')
    REDIS_DB = os.getenv('REDIS_DB', '0')


class DockerConfig(DevelopmentConfig):
    PORT = 80
    ACTION_SERVICE = 'http://action:8151'
    COLLECTION_EXERCISE_SERVICE = 'http://collex:8145'
    COLLECTION_INSTRUMENT_SERVICE = 'http://collection-instrument:8002'
    SAMPLE_SERVICE = 'http://sample:8125'
    SURVEY_SERVICE = 'http://survey:8080'
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'rabbitmq')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '5672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'Case.CaseDelivery')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    REDIS_HOST = os.getenv('REDIS_SERVICE_HOST', 'redis')
    REDIS_PORT = os.getenv('REDIS_SERVICE_PORT', '6379')
    REDIS_DB = os.getenv('REDIS_DB', '0')
