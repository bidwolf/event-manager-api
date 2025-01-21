import pytest

from src.modules.events.dao.attendee import AttendeeDAO
from src.modules.events.entities.attendee import AttendeeEntity
from src.modules.events.exc.attendee import AttendeeAlreadyExistsError
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_register_attendee(connection):
    dao = AttendeeDAO(connection=connection)
    knowed_id = "e7ff0523-e83e-4b31-b701-ded34ff360b6"
    new_attendee = AttendeeEntity(
        email="test2@gmail.com",
        event_id=knowed_id,
        name="test name",
        checked_in_at=None,
        attendee_id=None,
        created_at=None,
    )
    result = dao.register_participant(attendee=new_attendee)
    assert result is not None
    print(result.id)
    with pytest.raises(AttendeeAlreadyExistsError) as exc:
        dao.register_participant(attendee=new_attendee)
    assert (
        str(exc.value)
        == "An attendee with the given email is already registered in this event."
    )
