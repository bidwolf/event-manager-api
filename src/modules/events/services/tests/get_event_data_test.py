from datetime import datetime
from unittest.mock import MagicMock

from pytest import raises
from src.modules.events.dtos.event import EventDTO
from src.modules.events.entities.event import EventAttributes, EventEntity
from src.modules.events.exc.event import EventNotFoundError
from src.modules.events.repositories.event import EventRepositoryInterface
from src.modules.events.services.event import EventService


class TestGetEventData:
    def setup_method(self):
        self.repository = MagicMock(spec=EventRepositoryInterface)
        self.event_found_data = EventAttributes(
            {
                "title": "event title",
                "details": "Test",
                "maximum_attendees": 2,
                "slug": "test-slug",
                "created_at": datetime(2024, 12, 12),
            }
        )
        self.event_found = EventEntity(**self.event_found_data)

    def test_retrieve_event_data(self):
        self.repository.get_event_by_id.return_value = self.event_found
        service = EventService(repository=self.repository)
        event_data = service.get_event_data(event_id=self.event_found.id)
        assert isinstance(event_data, EventDTO)
        assert event_data.title == self.event_found_data["title"]
        assert event_data.details == self.event_found_data["details"]
        assert (
            event_data.maximum_attendees == self.event_found_data["maximum_attendees"]
        )
        assert event_data.slug == self.event_found_data["slug"]
        assert event_data.event_id == self.event_found.id
        assert event_data.created_at == self.event_found.created_at
        self.repository.get_event_by_id.assert_called_once_with(
            event_id=self.event_found.id
        )

    def test_retrieve_event_data_fails(self):
        self.repository.get_event_by_id.return_value = None
        service = EventService(repository=self.repository)
        with raises(EventNotFoundError) as exc:
            service.get_event_data(event_id="1")
        self.repository.get_event_by_id.assert_called_with(event_id="1")
        assert str(exc.value) == "Event not found."
