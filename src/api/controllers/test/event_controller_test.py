from datetime import datetime
from http import HTTPStatus
from unittest.mock import MagicMock

from pytest import raises

from src.api.controllers.event import EventController
from src.api.types import HttpRequest
from src.modules.events.dtos.event import EventDTO, EventRegistrationDTO
from src.modules.events.exc.http import (
    HttpResponseError,
)
from src.modules.events.services.event import EventServiceInterface


class TestEventController:
    def setup_method(self):
        self.service = MagicMock(spec=EventServiceInterface)

    def test_get_event_without_params(self):
        controller = EventController(service=self.service)
        request = HttpRequest(body=None)
        with raises(HttpResponseError) as exc:
            controller.get_event(request=request)
        self.service.get_event_data.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You should provide the 'event_id' parameter."

    def test_get_event_without_event_id_parameter(self):
        controller = EventController(service=self.service)
        request = HttpRequest(body=None, params={})
        with raises(HttpResponseError) as exc:
            controller.get_event(request=request)
        self.service.get_event_data.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You should provide the 'event_id' parameter."

    def test_get_event_with_invalid_event_id_parameter(self):
        controller = EventController(service=self.service)
        request = HttpRequest(body=None, params={"event_id": 333})
        with raises(HttpResponseError) as exc:
            controller.get_event(request=request)
        self.service.get_event_data.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == "You provided an invalid event id."

    def test_get_event_not_found(self):
        controller = EventController(service=self.service)
        request = HttpRequest(body=None, params={"event_id": "333"})
        self.service.get_event_data.return_value = None
        with raises(HttpResponseError) as exc:
            controller.get_event(request=request)
        self.service.get_event_data.assert_called_with(
            event_id=request.params["event_id"]
        )

        assert exc.value.status == HTTPStatus.NOT_FOUND
        assert exc.value.details == "Event not found."

    def test_get_event(self):
        controller = EventController(service=self.service)
        request = HttpRequest(body=None, params={"event_id": "333"})
        event_response = EventDTO(
            created_at=datetime.now(),
            details="anything",
            event_id=request.params["event_id"],
            maximum_attendees=None,
            slug="any-slug",
            title="any title",
        )
        self.service.get_event_data.return_value = event_response

        result = controller.get_event(request=request)
        self.service.get_event_data.assert_called_with(
            event_id=request.params["event_id"]
        )

        assert result.status == HTTPStatus.OK
        assert result.payload["event"] == event_response

    def test_register_event_not_created(self):
        controller = EventController(service=self.service)
        request = HttpRequest(
            body={
                "title": "test title",
                "slug": "test-slug",
                "details": "nothing",
                "maximum_attendees": 5,
            }
        )
        input_data = EventRegistrationDTO(**request.body)
        response_data = None
        self.service.create_event.return_value = response_data
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_called_once_with(data=input_data)
        assert exc.value.status == HTTPStatus.SERVICE_UNAVAILABLE
        assert exc.value.details == "An error ocurred while creating the event."

    def test_register_event_without_body(self):
        controller = EventController(service=self.service)
        request = HttpRequest(body=None)
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.BAD_REQUEST
        assert exc.value.details == (
            "The request should have the required fields:\n"
            " - 'title' : a string with at least 3 chracteres.\n"
            " - 'slug': a string with at least 3 chracteres.\n"
            " - 'details': [Optional] should be a string.\n"
            " - 'maximum_attendees': [Optional] should be an integer.\n"
        )

    def test_register_event_with_invalid_title(self):
        controller = EventController(service=self.service)
        request = HttpRequest(
            body={
                "title": None,
                "slug": "test-slug",
                "details": "nothing",
                "maximum_attendees": 5,
            }
        )
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event title is missing."
        request.body["title"] = 3
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event title is missing."
        request.body["title"] = "a"
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event title should have at least 3 characters."

    def test_register_event_with_invalid_slug(self):
        controller = EventController(service=self.service)
        request = HttpRequest(
            body={
                "title": "test valid",
                "slug": None,
                "details": "nothing",
                "maximum_attendees": 5,
            }
        )
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event slug is missing."
        request.body["slug"] = 3
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event slug is missing."
        request.body["slug"] = "a"
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "The event slug should have at least 3 characters."

    def test_register_event_with_invalid_details(self):
        controller = EventController(service=self.service)
        request = HttpRequest(
            body={
                "title": "test valid",
                "slug": "test-slug",
                "details": 3,
                "maximum_attendees": 5,
            }
        )
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "'details' should be a string."

    def test_register_event_with_invalid_maximum_attendees(self):
        controller = EventController(service=self.service)
        request = HttpRequest(
            body={
                "title": "test valid",
                "slug": "test-slug",
                "details": 3,
                "maximum_attendees": "5",
            }
        )
        with raises(HttpResponseError) as exc:
            controller.create_event(request=request)
        self.service.create_event.assert_not_called()
        assert exc.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert exc.value.details == "'maximum attendees' should be an integer."

    def test_register_event(self):
        controller = EventController(service=self.service)
        request = HttpRequest(
            body={
                "title": "test title",
                "slug": "test-slug",
                "details": "nothing",
                "maximum_attendees": 5,
            }
        )
        input_data = EventRegistrationDTO(**request.body)
        response_data = EventDTO(
            created_at=datetime.now,
            title=request.body.get("title"),
            details=request.body.get("details"),
            maximum_attendees=request.body.get("maximum_attendees"),
            slug=request.body.get("slug"),
            event_id="any-id",
        )
        self.service.create_event.return_value = response_data
        response = controller.create_event(request=request)
        self.service.create_event.assert_called_once_with(data=input_data)
        assert response.payload["created_event"] == response_data
        assert response.status == HTTPStatus.OK
