from http import HTTPMethod
from flask import Blueprint, request, jsonify

from src.api.composer.event import event_composer
from src.api.types import HttpRequest, HttpResponse
from src.modules.events.exc.http import HttpResponseError

event_blueprint = Blueprint("event", __name__)
event_controller = event_composer()


@event_blueprint.route("/events", methods=[HTTPMethod.POST])
def create_event_route():
    try:
        data_json = request.get_json()
        data_request = HttpRequest(body=data_json, params=None)
        response = event_controller.create_event(request=data_request)
        return (jsonify(response.payload), response.status)

    except HttpResponseError as exc:
        response = HttpResponse(
            payload={"title": exc.title, "details": exc.details}, status=exc.status
        )
        return (jsonify(response.payload), response.status)


@event_blueprint.route("/events", methods=[HTTPMethod.GET])
def get_event_routes():
    try:
        data_request = HttpRequest(
            body=None,
            params={
                "page_offset": request.args.get("page_offset", "0", type=str),
                "query": request.args.get("query", "", type=str),
            },
        )
        response = event_controller.get_events(request=data_request)
        return (jsonify(response.payload), response.status)

    except HttpResponseError as exc:
        response = HttpResponse(
            payload={"title": exc.title, "details": exc.details}, status=exc.status
        )
        return (jsonify(response.payload), response.status)


@event_blueprint.route("/events/<event_id>", methods=[HTTPMethod.GET])
def get_event_route(event_id):
    try:
        data_request = HttpRequest(body=None, params={"event_id": event_id})
        response = event_controller.get_event(request=data_request)
        return (jsonify(response.payload), response.status)

    except HttpResponseError as exc:
        response = HttpResponse(
            payload={"title": exc.title, "details": exc.details}, status=exc.status
        )
        return (jsonify(response.payload), response.status)
