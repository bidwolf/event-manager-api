from datetime import datetime
from unittest.mock import MagicMock
from pytest import fixture

from src.modules.events.dao.attendee import AttendeeDaoInterface
from src.modules.events.entities.attendee import AttendeeEntity
from src.modules.events.repositories.attendee import AttendeeRepository


@fixture(name="dao")
def attendee_dao():
    dao = MagicMock(spec=AttendeeDaoInterface)
    return dao


input_data = AttendeeEntity(
    name="test",
    email="mail@gmail.com",
    created_at=None,
    attendee_id=None,
    checked_in_at=None,
    event_id="12",
)
result = AttendeeEntity(
    name="test",
    email="mail@gmail.com",
    created_at=datetime.now(),
    attendee_id="12",
    checked_in_at=datetime.now(),
    event_id="12",
)


def test_create_attendee_repository(dao: MagicMock):
    repository = AttendeeRepository(dao=dao)

    dao.register_participant.return_value = result
    created = repository.create(data=input_data)
    dao.register_participant.assert_called_once_with(attendee=input_data)
    assert created == result


def test_get_event_participants_repository(dao: MagicMock):
    repository = AttendeeRepository(dao=dao)

    dao.get_event_participants.return_value = result
    created = repository.get_event_participants(event_id=input_data.event_id)
    dao.get_event_participants.assert_called_once_with(event_id=input_data.event_id)
    assert created == result


def test_get_attendee_by_id_repository(dao: MagicMock):
    repository = AttendeeRepository(dao=dao)

    dao.get_attendee_data.return_value = result
    created = repository.get_attendee_by_id(attendee_id=input_data.id)
    dao.get_attendee_data.assert_called_once_with(attendee_id=input_data.id)
    assert created == result
