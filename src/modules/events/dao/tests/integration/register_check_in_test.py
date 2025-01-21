import pytest
from src.modules.events.dao.check_in import CheckInDAO
from src.modules.events.exc.check_in import CheckInNotRegistered
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_register_attendee(connection):
    dao = CheckInDAO(connection=connection)
    knowed_id = "e6bbe25b-f8e7-40f7-8770-cb18b8ec3f43"
    result = dao.register_check_in(attendee_id=knowed_id)
    assert result is not None
    print(result.check_in_id)
    with pytest.raises(CheckInNotRegistered) as exc:
        dao.register_check_in(attendee_id=knowed_id)
    assert str(exc.value) == "Attendee already made check-in."
