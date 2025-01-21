from abc import ABC, abstractmethod
from http import HTTPStatus
from src.api.types import HttpRequest, HttpResponse
from src.modules.events.dtos.attendee import AttendeeRegistrationDTO
from src.modules.events.exc.attendee import (
    AttendeeNotCreatedError,
    AttendeeNotFoundError,
)
from src.modules.events.exc.http import map_exception_to_http_response
from src.modules.events.services.attendee import AttendeeServiceInterface


class AttendeeControllerInterface(ABC):
    @abstractmethod
    def register_attendee(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    def get_event_participants(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    def get_attendee_badge(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError


class AttendeeController(AttendeeControllerInterface):
    def __init__(self, service: AttendeeServiceInterface):
        self.__service = service

    def get_attendee_badge(self, request):
        try:
            if not (
                request.params
                and request.params["attendee_id"]
                and isinstance(request.params["attendee_id"], str)
            ):
                raise TypeError("You provided an invalid attendee id.")
            data = self.__service.get_attendee_event_credential(
                attendee_id=request.params["attendee_id"]
            )
            if not data:
                raise AttendeeNotFoundError(
                    "Cannot find the attendee badge for this attendee."
                )
            response_payload = {"badge_data": data}
            return HttpResponse(payload=response_payload, status=HTTPStatus.OK)

        except Exception as exc:
            raise map_exception_to_http_response(exc) from exc

    def get_event_participants(self, request):
        try:
            if not (
                request.params
                and request.params["event_id"]
                and isinstance(request.params["event_id"], str)
            ):
                raise TypeError("You provided an invalid event id.")
            data = self.__service.get_event_attendees(
                event_id=request.params["event_id"]
            )
            result_payload = {
                "attendees": data or [],
                "total": len(data) if data else 0,
            }
            return HttpResponse(payload=result_payload, status=HTTPStatus.OK)
        except Exception as exc:
            raise map_exception_to_http_response(exc) from exc

    def register_attendee(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.body:
                raise TypeError(
                    "The request should have the required fields:\n"
                    " - 'name' : minimum of 4 chracteres without numbers or special chracteres\n"
                    " - 'email': a valid email string\n"
                )
            if not (request.params and request.params.get("event_id")):
                raise TypeError("You should provide the 'event_id' route parameter")
            data = AttendeeRegistrationDTO(
                email=request.body.get("email", ""),
                event_id=request.params.get("event_id", ""),
                name=request.body.get("name", ""),
            )
            result_data = self.__service.register_attendee_in_event(data=data)
            if not result_data:
                raise AttendeeNotCreatedError(
                    message="An error occurs while registering the given attendee."
                )
            response_payload = {"attendee": result_data}
            return HttpResponse(payload=response_payload, status=HTTPStatus.OK)
        except Exception as exc:
            raise map_exception_to_http_response(exc) from exc
