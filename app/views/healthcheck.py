from flask import Blueprint, Response

blueprint = Blueprint('healthcheck', __name__, template_folder='templates')


@blueprint.route('/info', methods=["GET"])
def get_survey():
    return Response(status=200)
