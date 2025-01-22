from datetime import datetime
from unittest.mock import MagicMock

from pytest import raises
from src.modules.events.dtos.attendee import AttendeeDTO
from src.modules.events.entities.attendee import AttendeeEntity
from src.modules.events.exc.event import EventNotFoundError
from src.modules.events.repositories.attendee import AttendeeRepositoryInterface
from src.modules.events.services.attendee import AttendeeService
from src.modules.events.services.event import EventServiceInterface


class TestGetEventParticipants:
    def setup_method(self):
        self.repository = MagicMock(spec=AttendeeRepositoryInterface)
        self.event_service = MagicMock(spec=EventServiceInterface)
        self.participants = [
            AttendeeEntity(
                attendee_id="cool id",
                created_at=datetime(2024, 11, 11),
                email="juninho@gmail.com",
                event_id="1",
                name="Juninho",
                checked_in_at=None,
            )
        ]

    def test_get_event_participants(self):
        self.repository.get_event_participants.return_value = self.participants
        self.event_service.check_event_existence.return_value = True
        service = AttendeeService(
            repository=self.repository, event_service=self.event_service
        )
        offset = 1
        query = ""
        participants = service.get_event_attendees(
            event_id="1", query=query, offset=offset
        )
        self.event_service.check_event_existence.assert_called_once_with(event_id="1")
        self.repository.get_event_participants.assert_called_once_with(
            event_id="1", query=query, offset=offset
        )
        assert len(participants) > 0
        assert isinstance(participants[0], AttendeeDTO)

    def test_get_event_participants_fails_when_event_not_exists(self):
        self.repository.get_event_participants.return_value = self.participants
        self.event_service.check_event_existence.return_value = False
        service = AttendeeService(
            repository=self.repository, event_service=self.event_service
        )
        query = ""
        offset = 2
        with raises(EventNotFoundError) as exc:
            service.get_event_attendees(event_id="1", query=query, offset=offset)
        self.event_service.check_event_existence.assert_called_once_with(event_id="1")
        self.repository.get_event_participants.assert_not_called()
        assert str(exc.value) == "The given event not exists."
