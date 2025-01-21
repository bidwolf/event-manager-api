import pytest

from src.modules.events.dao.attendee import AttendeeDAO
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_get_all_attendees(connection):
    dao = AttendeeDAO(connection=connection)
    knowed_id = "9c6457ae-27ce-4172-bfcf-a349949b3ac6"
    event_participants = dao.get_event_participants(event_id=knowed_id)
    assert event_participants is not None
    assert len(event_participants) > 0


@pytest.mark.skip(reason="Database integration")
def test_empty_attendees_list_for_invalid_event_id(connection):
    dao = AttendeeDAO(connection=connection)
    unknowed_id = "any id"
    event_participants = dao.get_event_participants(event_id=unknowed_id)
    assert len(event_participants) == 0
