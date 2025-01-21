from abc import ABC, abstractmethod
from http import HTTPStatus


from src.api.types import HttpRequest, HttpResponse
from src.modules.events.exc.check_in import CheckInNotRegistered
from src.modules.events.exc.http import map_exception_to_http_response
from src.modules.events.services.check_in import CheckInServiceInterface


class CheckInControllerInterface(ABC):
    @abstractmethod
    def make_checkin(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError


class CheckInController(CheckInControllerInterface):
    def __init__(self, service: CheckInServiceInterface):
        self.__service = service

    def make_checkin(self, request):
        try:
            if not request.params or not request.params.get("attendee_id"):
                raise TypeError("You should provide the attendee_id parameter.")
            attendee_id = request.params.get("attendee_id")
            if not isinstance(attendee_id, str):
                raise TypeError("'attendee_id' should be a string.")
            check_in = self.__service.make_event_check_in(
                attendee_id=request.params["attendee_id"]
            )
            if not check_in:
                raise CheckInNotRegistered(
                    "Cannot register check-in for this attendee."
                )
            response_payload = {"check_in": check_in}
            return HttpResponse(payload=response_payload, status=HTTPStatus.OK)
        except Exception as exc:
            raise map_exception_to_http_response(exc=exc) from exc
