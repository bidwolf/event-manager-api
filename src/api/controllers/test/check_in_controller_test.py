from datetime import datetime
from http import HTTPStatus
from unittest.mock import MagicMock

from pytest import raises

from src.api.controllers.check_in import CheckInController
from src.api.types import HttpRequest
from src.modules.events.dtos.check_in import CheckInDTO
from src.modules.events.exc.http import (
    HttpResponseError,
)
from src.modules.events.services.check_in import CheckInServiceInterface


class TestCheckInController:
    def setup_method(self):
        self.service = MagicMock(spec=CheckInServiceInterface)

    def test_make_check_in(self):
        controller = CheckInController(service=self.service)
        request = HttpRequest(body=None, params={"attendee_id": "23"})
        service_result = CheckInDTO(
            attendee_id=request.params["attendee_id"],
            check_in_id=22,
            created_at=datetime.now(),
        )
        self.service.make_event_check_in.return_value = service_result
        response = controller.make_checkin(request=request)
        self.service.make_event_check_in.assert_called_with(
            attendee_id=request.params["attendee_id"]
        )
        assert response.payload["check_in"] == service_result

    def test_make_check_in_not_created(self):
        controller = CheckInController(service=self.service)
        request = HttpRequest(body=None, params={"attendee_id": "23"})
        service_result = None
        self.service.make_event_check_in.return_value = service_result
        with raises(HttpResponseError) as exc:
            controller.make_checkin(request=request)
        self.service.make_event_check_in.assert_called_with(
            attendee_id=request.params["attendee_id"]
        )
        assert exc.value.status == HTTPStatus.SERVICE_UNAVAILABLE
        assert exc.value.details == "Cannot register check-in for this attendee."

    def test_make_check_in_without_params(self):
        controller = CheckInController(service=self.service)
        request = HttpRequest(body=None, params=None)
        with raises(HttpResponseError) as exc:
            controller.make_checkin(request=request)
        self.service.make_event_check_in.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You should provide the attendee_id parameter."

    def test_make_check_in_with_param_without_attendee_id(self):
        controller = CheckInController(service=self.service)
        request = HttpRequest(body=None, params={"apple": "pen"})
        with raises(HttpResponseError) as exc:
            controller.make_checkin(request=request)
        self.service.make_event_check_in.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You should provide the attendee_id parameter."

    def test_make_check_in_with_param_with_invalid_attendee_id_type(self):
        controller = CheckInController(service=self.service)
        request = HttpRequest(body=None, params={"attendee_id": 737})
        with raises(HttpResponseError) as exc:
            controller.make_checkin(request=request)
        self.service.make_event_check_in.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "'attendee_id' should be a string."
