import pytest

from src.modules.events.dao.event import EventDAO
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_check_attendee_existent_in_event(connection):
    dao = EventDAO(connection=connection)
    existing_event_id = "e7ff0523-e83e-4b31-b701-ded34ff360b6"
    existent_email = "test2@gmail.com"
    event = dao.check_attendee_in_event(
        event_id=existing_event_id, attendee_email=existent_email
    )
    assert event is True


@pytest.mark.skip(reason="Database integration")
def test_check_attendee_with_non_existent_event(connection):
    dao = EventDAO(connection=connection)
    non_existent_event_id = "non existent event"
    existent_email = "test2@gmail.com"
    event = dao.check_attendee_in_event(
        event_id=non_existent_event_id, attendee_email=existent_email
    )
    assert event is False


@pytest.mark.skip(reason="Database integration")
def test_check_attendee_with_non_existent_email(connection):
    dao = EventDAO(connection=connection)
    existing_event_id = "e7ff0523-e83e-4b31-b701-ded34ff360b6"
    non_existent_email = "inexistent@gmail.com"
    event = dao.check_attendee_in_event(
        event_id=existing_event_id, attendee_email=non_existent_email
    )
    assert event is False
