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
            attendee_id = request.params["attendee_id"]
            data = self.__service.get_attendee_event_credential(attendee_id=attendee_id)
            if not data:
                raise AttendeeNotFoundError(
                    "Cannot find the attendee badge for this attendee."
                )
            qrcode_url = None
            if request.options and request.options.get("base_url"):
                qrcode_url = f"{request.options.get("base_url")}/{attendee_id}/check-in"
            response_payload = {
                "badge_data": {
                    "name": data.name,
                    "email": data.email,
                    "event_title": data.event_title,
                    "qrcode_url": qrcode_url,
                }
            }
            return HttpResponse(payload=response_payload, status=HTTPStatus.OK)

        except Exception as exc:
            raise map_exception_to_http_response(exc) from exc

    def get_event_participants(self, request):
        try:
            if not (
                request.params
                and request.params.get("event_id", None)
                and isinstance(request.params.get("event_id", None), str)
            ):
                raise TypeError("You provided an invalid event id.")
            query = request.params.get("query", "")
            event_id = request.params.get("event_id", None)
            offset = 0
            if str(request.params.get("page_offset", None)).isnumeric():
                offset = int(request.params.get("page_offset"))
            total = self.__service.get_total_attendees_in_event(
                event_id=event_id, query=query
            )
            data = self.__service.get_event_attendees(
                event_id=event_id, offset=offset, query=query
            )
            result_payload = {
                "attendees": data or [],
                "total": total,
                "page_offset": offset,
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
