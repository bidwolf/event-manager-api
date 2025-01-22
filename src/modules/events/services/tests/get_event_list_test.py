from datetime import datetime
from unittest.mock import MagicMock

from src.modules.events.dtos.event import EventDTO
from src.modules.events.entities.event import EventAttributes, EventEntity
from src.modules.events.repositories.event import EventRepositoryInterface
from src.modules.events.services.event import EventService


class TestGetEventList:
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
        self.event_list = [EventEntity(**self.event_found_data)]

    def test_retrieve_event_list(self):
        self.repository.load_events_list.return_value = self.event_list
        service = EventService(repository=self.repository)
        event_data = service.list_events(offset=2, query="")
        assert isinstance(event_data[0], EventDTO)
        assert event_data[0].title == self.event_found_data["title"]
        assert event_data[0].details == self.event_found_data["details"]
        assert (
            event_data[0].maximum_attendees
            == self.event_found_data["maximum_attendees"]
        )
        assert event_data[0].slug == self.event_found_data["slug"]
        assert event_data[0].event_id == self.event_list[0].id
        assert event_data[0].created_at == self.event_list[0].created_at
        self.repository.load_events_list.assert_called_once_with(offset=2, query="")
