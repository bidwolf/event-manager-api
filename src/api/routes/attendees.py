from http import HTTPMethod
from flask import Blueprint, request, jsonify

from src.api.composer.attendee import attendee_composer
from src.api.types import HttpRequest, HttpResponse
from src.modules.events.exc.http import HttpResponseError

attendee_blueprint = Blueprint("attendee", __name__)
attendee_controller = attendee_composer()


@attendee_blueprint.route("/events/<event_id>/attendee", methods=[HTTPMethod.POST])
def create_attendee(event_id):
    try:
        data_json = request.get_json()
        data_request = HttpRequest(body=data_json, params={"event_id": event_id})
        response = attendee_controller.register_attendee(request=data_request)
        return (jsonify(response.payload), response.status)

    except HttpResponseError as exc:
        response = HttpResponse(
            payload={"title": exc.title, "details": exc.details}, status=exc.status
        )
        return (jsonify(response.payload), response.status)


@attendee_blueprint.route("/events/<event_id>/attendees", methods=[HTTPMethod.GET])
def get_participants(event_id):
    try:
        data_request = HttpRequest(
            body=None,
            params={
                "event_id": event_id,
                "page_offset": request.args.get("page_offset", "0", type=str),
                "query": request.args.get("query", "", type=str),
            },
        )
        response = attendee_controller.get_event_participants(request=data_request)
        return (jsonify(response.payload), response.status)

    except HttpResponseError as exc:
        response = HttpResponse(
            payload={"title": exc.title, "details": exc.details}, status=exc.status
        )
        return (jsonify(response.payload), response.status)


@attendee_blueprint.route("/attendees/<attendee_id>/badge", methods=[HTTPMethod.GET])
def get_badge(attendee_id):
    try:
        data_request = HttpRequest(
            body=None,
            params={"attendee_id": attendee_id},
            options={"base_url": f"{request.host_url}/attendees"},
        )
        response = attendee_controller.get_attendee_badge(request=data_request)
        return (jsonify(response.payload), response.status)

    except HttpResponseError as exc:
        response = HttpResponse(
            payload={"title": exc.title, "details": exc.details}, status=exc.status
        )
        return (jsonify(response.payload), response.status)
