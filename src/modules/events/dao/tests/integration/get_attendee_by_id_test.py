import pytest

from src.modules.events.dao.attendee import AttendeeDAO
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_get_attendee_by_id(connection):
    dao = AttendeeDAO(connection=connection)
    knowed_id = "e6bbe25b-f8e7-40f7-8770-cb18b8ec3f43"
    attendee = dao.get_attendee_data(attendee_id=knowed_id)
    assert attendee is not None


@pytest.mark.skip(reason="Database integration")
def test_get_attendee_by_id_when_not_exists(connection):
    dao = AttendeeDAO(connection=connection)
    unknowed_id = "any id"
    attendee = dao.get_attendee_data(attendee_id=unknowed_id)
    assert attendee is None
