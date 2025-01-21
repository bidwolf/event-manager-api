from datetime import datetime
from unittest.mock import MagicMock
from pytest import fixture

from src.modules.events.dao.event import EventDaoInterface
from src.modules.events.entities.event import EventEntity
from src.modules.events.repositories.event import EventRepository


@fixture(name="dao")
def attendee_dao():
    dao = MagicMock(spec=EventDaoInterface)
    return dao


result = EventEntity(
    details="test",
    maximum_attendees=2,
    slug="123",
    title="test",
    created_at=datetime.now(),
    id="12",
)
input_data = EventEntity(
    details="test",
    maximum_attendees=2,
    slug="123",
    title="test",
    created_at=None,
    id=None,
)


def test_event_create(dao):
    dao.create_event.return_value = result
    repository = EventRepository(dao=dao)
    created = repository.create(data=input_data)
    dao.create_event.assert_called_with(event_data=input_data)
    assert created == result


def test_event_get_by_id(dao):
    dao.get_event_info.return_value = result
    repository = EventRepository(dao=dao)
    created = repository.get_event_by_id(event_id=input_data.id)
    dao.get_event_info.assert_called_with(event_id=input_data.id)
    assert created == result


def test_event_check_existence(dao):
    dao.check_event_exists.return_value = True
    repository = EventRepository(dao=dao)
    created = repository.check_event_existence(event_id=input_data.id)
    dao.check_event_exists.assert_called_with(event_id=input_data.id)
    assert created is True


def test_event_check_vacancy(dao):
    dao.check_event_has_vacancies.return_value = False
    repository = EventRepository(dao=dao)
    created = repository.check_event_capacity(event_id=input_data.id)
    dao.check_event_has_vacancies.assert_called_with(event_id=input_data.id)
    assert created is False


def test_event_check_participant_existence(dao):
    dao.check_attendee_in_event.return_value = False
    repository = EventRepository(dao=dao)
    created = repository.check_participant_existence(
        event_id=input_data.id, attendee_email="test@test.com"
    )
    dao.check_attendee_in_event.assert_called_with(
        event_id=input_data.id, attendee_email="test@test.com"
    )
    assert created is False
