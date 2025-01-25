from datetime import datetime
from http import HTTPStatus
from unittest.mock import MagicMock

from pytest import raises


from src.api.controllers.attendee import AttendeeController
from src.api.types import HttpRequest
from src.modules.events.dtos.attendee import AttendeeDTO, AttendeeRegistrationDTO


from src.modules.events.dtos.event_credentials import EventCredentialsDTO
from src.modules.events.exc.http import HttpResponseError
from src.modules.events.services.attendee import AttendeeServiceInterface


class TestAttendeeController:
    def setup_method(self):
        self.service = MagicMock(spec=AttendeeServiceInterface)

    def test_create_attendee_without_body(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None)
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == (
            "The request should have the required fields:\n"
            " - 'name' : minimum of 4 chracteres without numbers or special chracteres\n"
            " - 'email': a valid email string\n"
        )

    def test_create_attendee_with_invalid_params(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body={"name": 22, "email": "atest@gmail.com", "event_id": "33"}
        )
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You should provide the 'event_id' route parameter"

    def test_create_attendee_with_invalid_name(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body={"name": 22, "email": "atest@gmail.com", "event_id": "33"},
            params={"event_id": "teste"},
        )
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The name should be a string."
        request.body["name"] = "abc"
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The name is invalid."

    def test_create_attendee_with_invalid_event_id(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body={"name": "hernsssique", "email": "atest@gmail.com", "event_id": 33},
            params={"event_id": 3333},
        )
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event id should be a string."
        request.body["event_id"] = ""
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event id should be a string."

    def test_create_attendee_with_invalid_email(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body={"name": "henrique", "email": "a", "event_id": "33"},
            params={"event_id": "teste"},
        )
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The email is invalid."

    def test_create_attendee_not_created(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body={"name": "henrique", "email": "a@gmail.com"},
            params={"event_id": "teste"},
        )
        data = AttendeeRegistrationDTO(
            email=request.body["email"],
            name=request.body["name"],
            event_id=request.params["event_id"],
        )
        self.service.register_attendee_in_event.return_value = None
        with raises(HttpResponseError) as exc:
            controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_called_with(data=data)
        assert exc.value.status == HTTPStatus.SERVICE_UNAVAILABLE
        assert (
            exc.value.details == "An error occurs while registering the given attendee."
        )

    def test_create_attendee(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body={"name": "henrique", "email": "a@gmail.com", "event_id": "33"},
            params={"event_id": "teste"},
        )
        data = AttendeeRegistrationDTO(
            email=request.body["email"],
            name=request.body["name"],
            event_id=request.params["event_id"],
        )
        response = controller.register_attendee(request=request)
        self.service.register_attendee_in_event.assert_called_with(data=data)
        assert (
            response.payload["attendee"]
            is self.service.register_attendee_in_event.return_value
        )
        assert response.status == HTTPStatus.OK

    def test_get_event_participants_without_params(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params=None)
        with raises(HttpResponseError) as exc:
            controller.get_event_participants(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        self.service.get_total_attendees_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You provided an invalid event id."

    def test_get_event_participants_with_invalid_param(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params={})
        with raises(HttpResponseError) as exc:
            controller.get_event_participants(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        self.service.get_total_attendees_in_event.assert_not_called()

        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You provided an invalid event id."

    def test_get_event_participants_with_invalid_event_id(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params={"event_id": 267})
        with raises(HttpResponseError) as exc:
            controller.get_event_participants(request=request)
        self.service.register_attendee_in_event.assert_not_called()
        self.service.get_total_attendees_in_event.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You provided an invalid event id."

    def test_get_event_empty_participants_list(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body=None, params={"event_id": "267", "page_offset": 0, "query": ""}
        )
        self.service.get_event_attendees.return_value = None
        self.service.get_total_attendees_in_event.return_value = 0
        response = controller.get_event_participants(request=request)
        self.service.get_total_attendees_in_event.assert_called_with(
            event_id=request.params["event_id"], query=""
        )
        self.service.get_event_attendees.assert_called_with(
            event_id=request.params["event_id"],
            offset=request.params["page_offset"],
            query=request.params["query"],
        )
        assert response.payload["attendees"] == []
        assert response.payload["total"] == 0
        assert response.status == HTTPStatus.OK

    def test_get_event_participants(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params={"event_id": "267"})
        attendees = [
            AttendeeDTO(
                attendee_id="any",
                checked_in_at=datetime.now(),
                created_at=datetime.now(),
                email="any@email.com.br",
                event_id=request.params["event_id"],
                name="any name",
            )
        ]
        self.service.get_event_attendees.return_value = attendees
        self.service.get_total_attendees_in_event.return_value = 1
        response = controller.get_event_participants(request=request)
        self.service.get_total_attendees_in_event.assert_called_with(
            event_id=request.params["event_id"], query=""
        )
        self.service.get_event_attendees.assert_called_with(
            event_id=request.params["event_id"],
            offset=0,
            query="",
        )
        assert response.payload["attendees"] == attendees
        assert response.payload["total"] > 0
        assert response.status == HTTPStatus.OK

    def test_get_attendee_badge_without_params(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params=None)
        with raises(HttpResponseError) as exc:
            controller.get_attendee_badge(request=request)
        self.service.get_attendee_event_credential.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You provided an invalid attendee id."

    def test_get_attendee_badge_with_invalid_param(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params={})
        with raises(HttpResponseError) as exc:
            controller.get_attendee_badge(request=request)
        self.service.get_attendee_event_credential.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You provided an invalid attendee id."

    def test_get_attendee_badge_with_invalid_event_id(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params={"attendee_id": 267})
        with raises(HttpResponseError) as exc:
            controller.get_attendee_badge(request=request)
        self.service.get_attendee_event_credential.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You provided an invalid attendee id."

    def test_get_attendee_badge_not_found(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params={"attendee_id": "267"})
        self.service.get_attendee_event_credential.return_value = None
        with raises(HttpResponseError) as exc:
            controller.get_attendee_badge(request=request)
        self.service.get_attendee_event_credential.assert_called_with(
            attendee_id=request.params["attendee_id"]
        )
        assert exc.value.details == "Cannot find the attendee badge for this attendee."
        assert exc.value.status == HTTPStatus.NOT_FOUND

    def test_get_attendee_badge(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(
            body=None,
            params={"attendee_id": "267"},
            options={"base_url": "test://events"},
        )
        service_response = EventCredentialsDTO(
            event_title="asjdnasd",
            email="henrique@gmail.com",
            name="asdjaosd",
        )
        self.service.get_attendee_event_credential.return_value = service_response
        response = controller.get_attendee_badge(request=request)
        self.service.get_attendee_event_credential.assert_called_with(
            attendee_id=request.params["attendee_id"]
        )
        assert response.payload["badge_data"] == {
            "name": service_response.name,
            "qrcode_url": (
                f"{request.options["base_url"]}/{request.params["attendee_id"]}/check-in"
            ),
            "email": service_response.email,
            "event_title": service_response.event_title,
        }
        assert response.status == HTTPStatus.OK

    def test_get_attendee_badge_without_qrcode_url(self):
        controller = AttendeeController(service=self.service)
        request = HttpRequest(body=None, params={"attendee_id": "267"})
        service_response = EventCredentialsDTO(
            event_title="asjdnasd",
            email="henrique@gmail.com",
            name="asdjaosd",
        )
        self.service.get_attendee_event_credential.return_value = service_response
        response = controller.get_attendee_badge(request=request)
        self.service.get_attendee_event_credential.assert_called_with(
            attendee_id=request.params["attendee_id"]
        )
        assert response.payload["badge_data"] == {
            "name": service_response.name,
            "qrcode_url": None,
            "email": service_response.email,
            "event_title": service_response.event_title,
        }
        assert response.status == HTTPStatus.OK
