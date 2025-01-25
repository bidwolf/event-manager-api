from unittest.mock import MagicMock

from src.modules.events.repositories.attendee import AttendeeRepositoryInterface
from src.modules.events.services.attendee import AttendeeService
from src.modules.events.services.event import EventServiceInterface


class TestGetTotalEventParticipants:
    def setup_method(self):
        self.repository = MagicMock(spec=AttendeeRepositoryInterface)
        self.service = MagicMock(spec=EventServiceInterface)

    def test_evaluate_attendee_in_event(self):
        self.repository.get_total_event_participants.return_value = 1
        service = AttendeeService(
            repository=self.repository, event_service=EventServiceInterface
        )
        total = service.get_total_attendees_in_event(event_id="1", query="test")
        assert total is 1
        self.repository.get_total_event_participants.assert_called_once_with(
            event_id="1", query="test"
        )
