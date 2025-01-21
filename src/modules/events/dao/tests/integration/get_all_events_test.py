import pytest

from src.modules.events.dao.event import EventDAO
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_get_all_events(connection):
    dao = EventDAO(connection=connection)
    events = dao.get_all_events()
    for event in events:
        print(event.id)
    assert isinstance(events, list)
