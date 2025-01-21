from datetime import datetime
from unittest.mock import MagicMock

from pytest import raises
from src.modules.events.dtos.attendee import AttendeeDTO
from src.modules.events.entities.attendee import AttendeeAttributes, AttendeeEntity
from src.modules.events.exc.attendee import AttendeeNotFoundError
from src.modules.events.repositories.attendee import AttendeeRepositoryInterface
from src.modules.events.services.attendee import AttendeeService
from src.modules.events.services.event import EventServiceInterface


class TestGetAttendeeData:
    def setup_method(self):
        self.repository = MagicMock(spec=AttendeeRepositoryInterface)
        self.service = MagicMock(spec=EventServiceInterface)
        self.attendee_attributes = AttendeeAttributes(
            {
                "attendee_id": "1",
                "checked_in_at": datetime.now(),
                "created_at": datetime.now(),
                "email": "test@asdsa.com",
                "event_id": "22",
                "name": "Jonson",
            }
        )
        self.found_attendee_entity = AttendeeEntity(**self.attendee_attributes)

    def test_retrieve_event_data(self):
        self.repository.get_attendee_by_id.return_value = self.found_attendee_entity
        service = AttendeeService(
            event_service=self.service, repository=self.repository
        )
        attendee_event_data = service.get_attendee_data(
            attendee_id=self.found_attendee_entity.id
        )
        assert isinstance(attendee_event_data, AttendeeDTO)
        assert attendee_event_data.name == self.attendee_attributes["name"]
        assert (
            attendee_event_data.attendee_id == self.attendee_attributes["attendee_id"]
        )
        assert (
            attendee_event_data.checked_in_at
            == self.attendee_attributes["checked_in_at"]
        )
        assert attendee_event_data.created_at == self.attendee_attributes["created_at"]
        assert attendee_event_data.email == self.attendee_attributes["email"]
        assert attendee_event_data.event_id == self.attendee_attributes["event_id"]
        self.repository.get_attendee_by_id.assert_called_once_with(
            attendee_id=self.found_attendee_entity.id
        )

    def test_retrieve_event_data_fails(self):
        self.repository.get_attendee_by_id.return_value = None
        service = AttendeeService(
            event_service=self.service, repository=self.repository
        )
        with raises(AttendeeNotFoundError) as exc:
            service.get_attendee_data(attendee_id="1")
        self.repository.get_attendee_by_id.assert_called_with(attendee_id="1")
        assert str(exc.value) == "Attendee not found."
