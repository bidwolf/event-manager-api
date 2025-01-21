from datetime import datetime
from unittest.mock import MagicMock
from pytest import fixture

from src.modules.events.dao.check_in import CheckInDaoInterface
from src.modules.events.entities.check_in import CheckInEntity
from src.modules.events.repositories.check_in import CheckInRepository


@fixture(name="dao")
def attendee_dao():
    dao = MagicMock(spec=CheckInDaoInterface)
    return dao


result = CheckInEntity(
    check_in_id="id",
    created_at=datetime.now(),
    attendee_id="12",
)


def test_register_check_in_repository(dao: MagicMock):
    repository = CheckInRepository(dao=dao)

    dao.register_check_in.return_value = result
    created = repository.register_check_in(attendee_id="1")
    dao.register_check_in.assert_called_once_with(attendee_id="1")
    assert created == result
