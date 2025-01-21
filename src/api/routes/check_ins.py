from http import HTTPMethod
from flask import Blueprint, jsonify

from src.api.composer.check_in import check_in_composer
from src.api.types import HttpRequest, HttpResponse
from src.modules.events.exc.http import HttpResponseError

check_in_blueprint = Blueprint("check_in", __name__)
check_in_controller = check_in_composer()


@check_in_blueprint.route(
    "/attendees/<attendee_id>/check-in", methods=[HTTPMethod.POST]
)
def make_check_in_route(attendee_id):
    try:
        data_request = HttpRequest(body=None, params={"attendee_id": attendee_id})
        response = check_in_controller.make_checkin(request=data_request)
        return (jsonify(response.payload), response.status)

    except HttpResponseError as exc:
        response = HttpResponse(
            payload={"title": exc.title, "details": exc.details}, status=exc.status
        )
        return (jsonify(response.payload), response.status)
