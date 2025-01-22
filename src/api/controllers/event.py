from abc import ABC, abstractmethod
from http import HTTPStatus
from src.api.types import HttpRequest, HttpResponse
from src.modules.events.dtos.event import EventRegistrationDTO
from src.modules.events.exc.event import EventNotCreatedError, EventNotFoundError
from src.modules.events.exc.http import map_exception_to_http_response
from src.modules.events.services.event import EventServiceInterface


class EventControllerInterface(ABC):
    @abstractmethod
    def create_event(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    def get_event(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    def get_events(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError


class EventController(EventControllerInterface):
    def __init__(self, service: EventServiceInterface):
        self.__service = service

    def create_event(self, request):
        try:
            if not request.body:
                raise TypeError(
                    "The request should have the required fields:\n"
                    " - 'title' : a string with at least 3 chracteres.\n"
                    " - 'slug': a string with at least 3 chracteres.\n"
                    " - 'details': [Optional] should be a string.\n"
                    " - 'maximum_attendees': [Optional] should be an integer.\n"
                )
            input_data = EventRegistrationDTO(
                title=request.body.get("title", ""),
                details=request.body.get("details", ""),
                maximum_attendees=request.body.get("maximum_attendees", None),
                slug=request.body.get("slug"),
            )
            created_event = self.__service.create_event(data=input_data)
            if not created_event:
                raise EventNotCreatedError("An error ocurred while creating the event.")
            response_payload = {"created_event": created_event}
            return HttpResponse(payload=response_payload, status=HTTPStatus.OK)
        except Exception as exc:
            raise map_exception_to_http_response(exc=exc) from exc

    def get_event(self, request):
        try:
            if not request.params or not request.params["event_id"]:
                raise TypeError("You should provide the 'event_id' parameter.")
            event_id = request.params["event_id"]
            if not isinstance(event_id, str):
                raise TypeError("You provided an invalid event id.")
            event_found = self.__service.get_event_data(event_id=event_id)
            if not event_found:
                raise EventNotFoundError("Event not found.")
            response_payload = {"event": event_found}
            return HttpResponse(payload=response_payload, status=HTTPStatus.OK)
        except Exception as exc:
            raise map_exception_to_http_response(exc=exc) from exc

    def get_events(self, request):
        try:
            page_offset = 0
            query = ""
            if request.params:
                if str(request.params.get("page_offset", "0")).isdigit():
                    page_offset = int(request.params.get("page_offset", "0"))
                query = str(request.params.get("query", ""))
            events = self.__service.list_events(offset=page_offset, query=query)
            response_payload = {
                "events": events,
                "page_offset": page_offset,
                "quantity": len(events),
            }
            return HttpResponse(payload=response_payload, status=HTTPStatus.OK)

        except Exception as exc:
            raise map_exception_to_http_response(exc=exc) from exc
