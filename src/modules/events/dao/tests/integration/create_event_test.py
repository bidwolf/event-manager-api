import pytest

from src.modules.events.dao.event import EventDAO
from src.modules.events.entities.event import EventEntity
from src.modules.events.exc.event import EventAlreadyExistsError
from .fixture_connection import get_connection  # pylint: disable=unused-import


@pytest.mark.skip(reason="Database integration")
def test_create_event(connection):
    dao = EventDAO(connection=connection)
    new_event = EventEntity(
        title="Test awesome title",
        details="test awesome detail",
        slug="awesome slug",
        maximum_attendees=None,
        id=None,
        created_at=None,
    )
    result = dao.create_event(event_data=new_event)
    assert result is not None
    with pytest.raises(EventAlreadyExistsError) as exc:
        dao.create_event(event_data=new_event)
    assert str(exc.value) == "An event with this slug already exists."
