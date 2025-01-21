from unittest.mock import MagicMock
from src.modules.events.repositories.event import EventRepositoryInterface
from src.modules.events.services.event import EventService


class TestEvaluateAttendeeRegistration:
    def setup_method(self):
        self.repository = MagicMock(spec=EventRepositoryInterface)

    def test_retrieve_event_data(self):
        self.repository.check_participant_existence.return_value = True
        service = EventService(repository=self.repository)
        event_exists = service.check_attendee_in_event(
            attendee_email="henrique@ajskdhga.com", event_id="1"
        )
        assert event_exists is True
        self.repository.check_participant_existence.assert_called_once_with(
            attendee_email="henrique@ajskdhga.com", event_id="1"
        )

    def test_retrieve_event_data_fails(self):
        self.repository.check_participant_existence.return_value = False
        service = EventService(repository=self.repository)
        event_exists = service.check_attendee_in_event(
            attendee_email="henrique@ajskdhga.com", event_id="1"
        )
        self.repository.check_participant_existence.assert_called_once_with(
            attendee_email="henrique@ajskdhga.com", event_id="1"
        )
        assert event_exists is False
