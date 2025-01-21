import pytest

from src.modules.events.dao.event import EventDAO
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_event_has_vacancies(connection):
    dao = EventDAO(connection=connection)
    vacant_event_identifier = "e7ff0523-e83e-4b31-b701-ded34ff360b6"
    event = dao.check_event_has_vacancies(event_id=vacant_event_identifier)
    assert event is True


@pytest.mark.skip(reason="Database integration")
def test_sold_out_event_has_no_vacancies(connection):
    dao = EventDAO(connection=connection)
    sold_out_event_id = "9c6457ae-27ce-4172-bfcf-a349949b3ac6"
    event = dao.check_event_has_vacancies(event_id=sold_out_event_id)
    assert event is False
