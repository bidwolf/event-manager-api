from http import HTTPStatus

from src.modules.events.exc.attendee import (
    AttendeeAlreadyExistsError,
    AttendeeNotCreatedError,
    AttendeeNotFoundError,
)
from src.modules.events.exc.check_in import CheckInNotRegistered
from src.modules.events.exc.common import ValidationError
from src.modules.events.exc.event import EventNotCreatedError, EventNotFoundError


class HttpResponseError(Exception):
    def __init__(self, title: str, details: str, status: HTTPStatus):
        self.title = title
        self.details = details
        self.status = status
        super().__init__(details)


def map_exception_to_http_response(exc: Exception) -> HttpResponseError:
    error_mapping = {
        TypeError: (HTTPStatus.BAD_REQUEST, "Bad Request."),
        ValueError: (HTTPStatus.BAD_REQUEST, "Bad Request."),
        ValidationError: (
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "Unprocessable Entity.",
        ),
        AttendeeNotFoundError: (HTTPStatus.NOT_FOUND, "Not Found Event."),
        EventNotFoundError: (HTTPStatus.NOT_FOUND, "Not Found Event."),
        AttendeeAlreadyExistsError: (HTTPStatus.CONFLICT, "Attendee Already Exists."),
        AttendeeNotCreatedError: (
            HTTPStatus.SERVICE_UNAVAILABLE,
            "Service Unavailable",
        ),
        CheckInNotRegistered: (
            HTTPStatus.SERVICE_UNAVAILABLE,
            "Service Unavailable",
        ),
        EventNotCreatedError: (
            HTTPStatus.SERVICE_UNAVAILABLE,
            "Service Unavailable",
        ),
    }

    status, title = error_mapping.get(
        type(exc), (HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Server Error.")
    )
    return HttpResponseError(details=str(exc), title=title, status=status)
