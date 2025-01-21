from unittest.mock import MagicMock
from src.modules.events.repositories.event import EventRepositoryInterface
from src.modules.events.services.event import EventService


class TestEvaluateCapacity:
    def setup_method(self):
        self.repository = MagicMock(spec=EventRepositoryInterface)

    def test_evaluate_attendee_in_event(self):
        self.repository.check_participant_existence.return_value = True
        service = EventService(repository=self.repository)
        event_has_capacity = service.check_attendee_in_event(
            event_id="1", attendee_email="test@test.com"
        )
        assert event_has_capacity is True
        self.repository.check_participant_existence.assert_called_once_with(
            event_id="1", attendee_email="test@test.com"
        )

    def test_retrieve_event_data_fails(self):
        self.repository.check_participant_existence.return_value = False
        service = EventService(repository=self.repository)
        event_has_capacity = service.check_attendee_in_event(
            event_id="1", attendee_email="test@test.com"
        )
        self.repository.check_participant_existence.assert_called_once_with(
            event_id="1", attendee_email="test@test.com"
        )
        assert event_has_capacity is False
