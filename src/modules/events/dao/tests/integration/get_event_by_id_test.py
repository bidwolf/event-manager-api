import pytest

from src.modules.events.dao.event import EventDAO
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_get_event_by_id(connection):
    dao = EventDAO(connection=connection)
    knowed_id = "9c6457ae-27ce-4172-bfcf-a349949b3ac6"
    event = dao.get_event_info(event_id=knowed_id)
    assert event is not None


@pytest.mark.skip(reason="Database integration")
def test_get_event_by_id_when_not_exists(connection):
    dao = EventDAO(connection=connection)
    unknowed_id = "any id"
    event = dao.get_event_info(event_id=unknowed_id)
    assert event is None
