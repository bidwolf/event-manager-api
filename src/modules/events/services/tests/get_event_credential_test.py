from datetime import datetime
from unittest.mock import MagicMock

from pytest import raises
from src.modules.events.dtos.event import EventDTO
from src.modules.events.dtos.event_credentials import EventCredentialsDTO
from src.modules.events.entities.attendee import AttendeeEntity
from src.modules.events.exc.attendee import AttendeeNotFoundError
from src.modules.events.exc.event import EventNotFoundError
from src.modules.events.repositories.attendee import AttendeeRepositoryInterface
from src.modules.events.services.attendee import AttendeeService
from src.modules.events.services.event import EventServiceInterface


class TestEventCredential:
    def setup_method(self):
        self.repository = MagicMock(spec=AttendeeRepositoryInterface)
        self.event_service = MagicMock(spec=EventServiceInterface)

    def test_get_event_credential_not_found_attendee(self):
        service = AttendeeService(
            repository=self.repository, event_service=self.event_service
        )
        attendee_id = "1"
        mocked_attendee_data = AttendeeEntity(
            attendee_id=attendee_id,
            name="test",
            email="test@gmail.com",
            event_id="id-2",
            created_at=datetime(2024, 2, 2),
            checked_in_at=datetime.now(),
        )
        self.repository.get_attendee_by_id.return_value = mocked_attendee_data
        self.event_service.get_event_data.return_value = None
        with raises(EventNotFoundError) as exc:
            service.get_attendee_event_credential(attendee_id=attendee_id)
        self.repository.get_attendee_by_id.assert_called_once_with(
            attendee_id=attendee_id
        )
        self.event_service.get_event_data.assert_called_once_with(
            event_id=mocked_attendee_data.event_id
        )
        assert str(exc.value) == "The registered event was not found."

    def test_get_event_credential_not_found_event(self):
        service = AttendeeService(
            repository=self.repository, event_service=self.event_service
        )
        attendee_id = "1"
        self.repository.get_attendee_by_id.return_value = None
        with raises(AttendeeNotFoundError) as exc:
            service.get_attendee_event_credential(attendee_id=attendee_id)
        self.repository.get_attendee_by_id.assert_called_once_with(
            attendee_id=attendee_id
        )
        self.event_service.get_event_data.assert_not_called()
        assert str(exc.value) == "Attendee not found."

    def test_get_event_credential(self):
        service = AttendeeService(
            repository=self.repository, event_service=self.event_service
        )
        attendee_id = "id-1"
        mocked_attendee_data = AttendeeEntity(
            attendee_id=attendee_id,
            name="test",
            email="test@gmail.com",
            event_id="id-2",
            created_at=datetime(2024, 2, 2),
            checked_in_at=datetime.now(),
        )
        mocked_event_data = EventDTO(
            created_at=datetime(2024, 1, 1),
            details="fancy detail",
            event_id=mocked_attendee_data.event_id,
            slug="fancy-slug",
            title="fancy title",
            maximum_attendees=99,
        )
        self.repository.get_attendee_by_id.return_value = mocked_attendee_data
        self.event_service.get_event_data.return_value = mocked_event_data
        credential = service.get_attendee_event_credential(attendee_id=attendee_id)
        assert isinstance(credential, EventCredentialsDTO)
        self.repository.get_attendee_by_id.assert_called_once_with(
            attendee_id=attendee_id
        )
        self.event_service.get_event_data.assert_called_once_with(
            event_id=mocked_attendee_data.event_id
        )
        assert credential.event_details == mocked_event_data.details
