from unittest.mock import MagicMock
from src.modules.events.repositories.event import EventRepositoryInterface
from src.modules.events.services.event import EventService


class TestEvaluateCapacity:
    def setup_method(self):
        self.repository = MagicMock(spec=EventRepositoryInterface)

    def test_retrieve_event_data(self):
        self.repository.check_event_capacity.return_value = True
        service = EventService(repository=self.repository)
        event_has_capacity = service.evaluate_event_capacity(event_id="1")
        assert event_has_capacity is True
        self.repository.check_event_capacity.assert_called_once_with(event_id="1")

    def test_retrieve_event_data_fails(self):
        self.repository.check_event_capacity.return_value = False
        service = EventService(repository=self.repository)
        event_has_capacity = service.evaluate_event_capacity(event_id="1")
        self.repository.check_event_capacity.assert_called_once_with(event_id="1")
        assert event_has_capacity is False
