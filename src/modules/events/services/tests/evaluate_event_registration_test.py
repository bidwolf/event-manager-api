from unittest.mock import MagicMock
from src.modules.events.repositories.event import EventRepositoryInterface
from src.modules.events.services.event import EventService


class TestEvaluateEventRegistration:
    def setup_method(self):
        self.repository = MagicMock(spec=EventRepositoryInterface)

    def test_retrieve_event_data(self):
        self.repository.check_event_existence.return_value = True
        service = EventService(repository=self.repository)
        event_exists = service.check_event_existence(event_id="1")
        assert event_exists is True
        self.repository.check_event_existence.assert_called_once_with(event_id="1")

    def test_retrieve_event_data_fails(self):
        self.repository.check_event_existence.return_value = False
        service = EventService(repository=self.repository)
        event_exists = service.check_event_existence(event_id="1")
        self.repository.check_event_existence.assert_called_once_with(event_id="1")
        assert event_exists is False
