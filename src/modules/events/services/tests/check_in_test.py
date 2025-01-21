from datetime import datetime
from unittest.mock import MagicMock, patch

from pytest import raises
from src.modules.events.dtos.attendee import AttendeeDTO
from src.modules.events.dtos.check_in import CheckInDTO
from src.modules.events.services.check_in import CheckInEntity
from src.modules.events.exc.attendee import AttendeeNotFoundError
from src.modules.events.exc.check_in import AlreadyCheckedInError, CheckInNotRegistered
from src.modules.events.repositories.check_in import CheckInRepositoryInterface
from src.modules.events.services.attendee import AttendeeServiceInterface
from src.modules.events.services.check_in import CheckInService


class TestCheckInRegistration:
    def setup_method(self):
        self.repository = MagicMock(spec=CheckInRepositoryInterface)
        self.service = MagicMock(spec=AttendeeServiceInterface)
        self.check_in_result = CheckInDTO(
            attendee_id="1", created_at=datetime.now(), check_in_id="good_id"
        )
        self.check_in_entity = CheckInEntity(
            attendee_id="1", created_at=datetime.now(), check_in_id="good_id"
        )

    def test_check_in(self):
        with patch(
            "src.modules.events.services.check_in.CheckInEntity",
            return_value=self.check_in_entity,
        ):
            self.repository.register_check_in.return_value = self.check_in_result
            self.service.get_attendee_data.return_value = AttendeeDTO(
                checked_in_at=None,
                attendee_id="1",
                event_id="2",
                created_at=datetime.now(),
                email="test@gmail.com",
                name="test",
            )
            service = CheckInService(
                repository=self.repository, attendee_service=self.service
            )
            result = service.make_event_check_in(attendee_id="1")
            assert result.attendee_id == self.check_in_result.attendee_id
            assert result.check_in_id == self.check_in_result.check_in_id
            assert result.created_at == self.check_in_result.created_at
            self.repository.register_check_in.assert_called_once_with(attendee_id="1")
            self.service.get_attendee_data.assert_called_once_with(attendee_id="1")

    def test_check_in_attendee_not_found(self):
        with patch(
            "src.modules.events.services.check_in.CheckInEntity",
            return_value=self.check_in_entity,
        ):
            self.service.get_attendee_data.return_value = None
            service = CheckInService(
                repository=self.repository, attendee_service=self.service
            )
            with raises(AttendeeNotFoundError) as exc:
                service.make_event_check_in(attendee_id="1")
            self.repository.register_check_in.assert_not_called()
            self.service.get_attendee_data.assert_called_once_with(attendee_id="1")
            assert (
                str(exc.value) == "The given attendee is not registered in any event."
            )

    def test_check_in_attendee_checked_in(self):
        with patch(
            "src.modules.events.services.check_in.CheckInEntity",
            return_value=self.check_in_entity,
        ):
            self.service.get_attendee_data.return_value = AttendeeDTO(
                checked_in_at=datetime.now(),
                attendee_id="1",
                event_id="2",
                created_at=datetime.now(),
                email="test@gmail.com",
                name="test",
            )
            service = CheckInService(
                repository=self.repository, attendee_service=self.service
            )
            with raises(AlreadyCheckedInError) as exc:
                service.make_event_check_in(attendee_id="1")
            self.repository.register_check_in.assert_not_called()
            self.service.get_attendee_data.assert_called_once_with(attendee_id="1")
            assert str(exc.value) == "Attendee has already made a check in."

    def test_check_in_attendee_not_registered(self):
        with patch(
            "src.modules.events.services.check_in.CheckInEntity",
            return_value=self.check_in_entity,
        ):
            self.repository.register_check_in.return_value = None
            self.service.get_attendee_data.return_value = AttendeeDTO(
                checked_in_at=None,
                attendee_id="1",
                event_id="2",
                created_at=datetime.now(),
                email="test@gmail.com",
                name="test",
            )
            service = CheckInService(
                repository=self.repository, attendee_service=self.service
            )
            with raises(CheckInNotRegistered) as exc:
                service.make_event_check_in(attendee_id="1")
            self.repository.register_check_in.assert_called_once()
            self.service.get_attendee_data.assert_called_once_with(attendee_id="1")
            assert str(exc.value) == "An error ocurred while making the checkin"
