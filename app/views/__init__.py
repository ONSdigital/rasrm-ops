from app.views import surveys, survey_classifier, survey, collection_exercise_events, collection_exercise, ci, \
    action, sample, healthcheck


def setup_blueprints(app):
    app.register_blueprint(healthcheck.blueprint)
    app.register_blueprint(surveys.blueprint)
    app.register_blueprint(survey_classifier.blueprint)
    app.register_blueprint(survey.blueprint)
    app.register_blueprint(collection_exercise.blueprint)
    app.register_blueprint(collection_exercise_events.blueprint)
    app.register_blueprint(ci.blueprint)
    app.register_blueprint(sample.blueprint)
    app.register_blueprint(action.blueprint)
