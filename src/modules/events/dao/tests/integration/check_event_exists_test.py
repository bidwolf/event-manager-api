import pytest

from src.modules.events.dao.event import EventDAO
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_verify_event_existence(connection):
    dao = EventDAO(connection=connection)
    existing_event_id = "e7ff0523-e83e-4b31-b701-ded34ff360b6"
    event = dao.check_event_exists(event_id=existing_event_id)
    assert event is True


@pytest.mark.skip(reason="Database integration")
def test_sold_out_event_has_no_vacancies(connection):
    dao = EventDAO(connection=connection)
    non_existent_event_id = "non existent event"
    event = dao.check_event_exists(event_id=non_existent_event_id)
    assert event is False
