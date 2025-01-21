from datetime import datetime
from unittest.mock import MagicMock, patch

from pytest import raises
from src.modules.events.dtos.event import EventDTO
from src.modules.events.entities.event import EventAttributes, EventEntity
from src.modules.events.exc.event import EventAlreadyExistsError, EventNotCreatedError
from src.modules.events.repositories.event import EventRepositoryInterface
from src.modules.events.services.event import EventService, EventServiceInterface


class TestEventCreation:
    def setup_method(self):
        self.repository = MagicMock(spec=EventRepositoryInterface)
        self.event_data = EventAttributes(
            {
                "title": "event title",
                "details": "Test",
                "maximum_attendees": 2,
                "slug": "test-slug",
                "created_at": datetime(2025, 1, 1),
                "id": "created id",
            }
        )
        self.new_event = EventEntity(**self.event_data)

    def test_event_creation(self):
        with patch(
            "src.modules.events.services.event.EventEntity", return_value=self.new_event
        ) as new_event:
            service = EventService(repository=self.repository)
            self.repository.create.return_value = new_event
            self.repository.check_event_existence.return_value = False
            created_event = service.create_event(self.new_event)
            self.repository.check_event_existence.assert_called_once_with(
                event_id=self.new_event.id
            )
            self.repository.create.assert_called_once_with(data=self.new_event)
            assert issubclass(EventService, EventServiceInterface)
            assert created_event.event_id == new_event.id
            assert created_event.title == new_event.title
            assert created_event.details == new_event.details
            assert created_event.maximum_attendees == new_event.maximum_attendees
            assert created_event.slug == new_event.slug
            assert isinstance(created_event, EventDTO) is True

    def test_event_creation_fails_while_creating(self):
        with patch(
            "src.modules.events.services.event.EventEntity", return_value=self.new_event
        ):
            service = EventService(repository=self.repository)
            self.repository.check_event_existence.return_value = False
            self.repository.create.return_value = None
            with raises(EventNotCreatedError) as exc:
                service.create_event(data=self.new_event)
            self.repository.check_event_existence.assert_called_once_with(
                event_id=self.new_event.id
            )
            self.repository.create.assert_called_once_with(data=self.new_event)
            assert str(exc.value) == "An error ocurred while creating the event."

    def test_event_creation_when_check_event_existence(self):
        with patch(
            "src.modules.events.services.event.EventEntity", return_value=self.new_event
        ):
            service = EventService(repository=self.repository)
            self.repository.check_event_existence.return_value = True
            with raises(EventAlreadyExistsError) as exc:
                service.create_event(data=self.new_event)
            self.repository.check_event_existence.assert_called_once_with(
                event_id=self.new_event.id
            )
            self.repository.create.assert_not_called()
            assert str(exc.value) == "This event is already registered."
