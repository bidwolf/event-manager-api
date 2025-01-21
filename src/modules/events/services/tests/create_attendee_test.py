from unittest.mock import MagicMock, patch

from pytest import raises

from src.modules.events.dtos.attendee import AttendeeDTO
from src.modules.events.entities.attendee import AttendeeAttributes, AttendeeEntity
from src.modules.events.exc.attendee import (
    AttendeeAlreadyExistsError,
    AttendeeNotCreatedError,
)
from src.modules.events.exc.event import EventNotFoundError, EventSoldOutError
from src.modules.events.repositories.attendee import AttendeeRepositoryInterface
from src.modules.events.services.attendee import AttendeeService
from src.modules.events.services.event import EventServiceInterface


class TestAttendeeCreation:
    def setup_method(self):
        self.repository = MagicMock(spec=AttendeeRepositoryInterface)
        self.event_service = MagicMock(spec=EventServiceInterface)
        self.attendee_attributes = AttendeeAttributes(
            {
                "email": "teste@gmail.com",
                "event_id": "23",
                "name": "teste",
                "attendee_id": None,
                "created_at": None,
                "checked_in_at": None,
            }
        )
        self.new_attendee = AttendeeEntity(**self.attendee_attributes)

    def test_attendee_creation(self):
        with patch(
            "src.modules.events.services.attendee.AttendeeEntity",
            return_value=self.new_attendee,
        ) as new_attendee:
            self.repository.create.return_value = new_attendee
            self.event_service.check_event_existence.return_value = True
            self.event_service.check_attendee_in_event.return_value = False
            self.event_service.evaluate_event_capacity.return_value = True
            service = AttendeeService(
                repository=self.repository, event_service=self.event_service
            )
            created_attendee = service.register_attendee_in_event(
                data=self.new_attendee
            )
            self.event_service.check_event_existence.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.event_service.check_attendee_in_event.assert_called_once_with(
                attendee_email=self.new_attendee.email,
                event_id=self.new_attendee.event_id,
            )
            self.event_service.evaluate_event_capacity.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.repository.create.assert_called_once_with(data=self.new_attendee)

            assert isinstance(created_attendee, AttendeeDTO)
            assert created_attendee.attendee_id is new_attendee.id
            assert created_attendee.name is new_attendee.name
            assert created_attendee.email is new_attendee.email
            assert created_attendee.event_id is new_attendee.event_id
            assert created_attendee.created_at is new_attendee.created_at

    def test_attendee_creation_when_event_not_exist(self):
        with patch(
            "src.modules.events.services.attendee.AttendeeEntity",
            return_value=self.new_attendee,
        ) as new_attendee:
            self.repository.create.return_value = new_attendee
            self.event_service.check_event_existence.return_value = False

            service = AttendeeService(
                repository=self.repository, event_service=self.event_service
            )
            with raises(EventNotFoundError) as exc:
                service.register_attendee_in_event(data=self.new_attendee)
            self.event_service.check_event_existence.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.event_service.check_attendee_in_event.assert_not_called()
            self.event_service.evaluate_event_capacity.assert_not_called()
            self.repository.create.assert_not_called()
            assert (
                str(exc.value)
                == "This registration failed because the given event was not Found."
            )

    def test_attendee_creation_when_attendee_is_already_registered(self):
        with patch(
            "src.modules.events.services.attendee.AttendeeEntity",
            return_value=self.new_attendee,
        ):
            self.repository.create.return_value = None
            self.event_service.check_event_existence.return_value = True
            self.event_service.check_attendee_in_event.return_value = True
            self.event_service.evaluate_event_capacity.return_value = False

            service = AttendeeService(
                repository=self.repository, event_service=self.event_service
            )
            with raises(AttendeeAlreadyExistsError) as exc:
                service.register_attendee_in_event(data=self.new_attendee)
            self.event_service.check_event_existence.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.event_service.evaluate_event_capacity.assert_not_called()
            self.repository.create.assert_not_called()
            assert str(exc.value) == "This attendee is already registered"

    def test_attendee_creation_when_event_is_crowded(self):
        with patch(
            "src.modules.events.services.attendee.AttendeeEntity",
            return_value=self.new_attendee,
        ):
            self.repository.create.return_value = None
            self.event_service.check_event_existence.return_value = True
            self.event_service.check_attendee_in_event.return_value = False
            self.event_service.evaluate_event_capacity.return_value = False

            service = AttendeeService(
                repository=self.repository, event_service=self.event_service
            )
            with raises(EventSoldOutError) as exc:
                service.register_attendee_in_event(data=self.new_attendee)
            self.event_service.check_event_existence.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.event_service.evaluate_event_capacity.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.repository.create.assert_not_called()
            assert (
                str(exc.value)
                == "This registration failed because the event has sold out."
            )

    def test_attendee_creation_fails_while_creating(self):
        with patch(
            "src.modules.events.services.attendee.AttendeeEntity",
            return_value=self.new_attendee,
        ):
            self.repository.create.return_value = None
            self.event_service.check_event_existence.return_value = True
            self.event_service.check_attendee_in_event.return_value = False
            self.event_service.evaluate_event_capacity.return_value = True
            service = AttendeeService(
                repository=self.repository, event_service=self.event_service
            )
            with raises(AttendeeNotCreatedError) as exc:
                service.register_attendee_in_event(data=self.new_attendee)
            self.event_service.check_event_existence.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.event_service.evaluate_event_capacity.assert_called_once_with(
                event_id=self.new_attendee.event_id
            )
            self.repository.create.assert_called_once_with(data=self.new_attendee)
            assert str(exc.value) == "An error ocurred while registering the attendee."
