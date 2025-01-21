from unittest.mock import patch, MagicMock
from pytest import raises
from sqlalchemy.exc import IntegrityError
from src.drivers.database.types import ConnectionInterface
from src.modules.events.dao.check_in import (
    CheckInDAO,
    CheckInEntity,
    CheckInNotRegistered,
)


class TestCheckDAOIn:
    def setup_method(self):
        self.mock_result = MagicMock()

    def test_register_check_in_success(self):
        with patch("src.modules.events.dao.check_in.text") as text:
            mock_connect = MagicMock(spec=ConnectionInterface)
            mock_connect.get_engine.return_value = MagicMock()
            engine = mock_connect.get_engine.return_value
            engine.connect.return_value = MagicMock()
            connection = engine.connect.return_value.__enter__.return_value
            connection.execute.return_value.first.return_value = (
                1,
                "2023-10-01 12:00:00",
                "123",
            )
            dao = CheckInDAO(connection=mock_connect)
            # Call the method
            attendee_id = "123"
            check_in = dao.register_check_in(attendee_id)
            mock_connect.get_engine.assert_called_once()
            # Assertions
            connection.execute.assert_called_once_with(
                text(
                    "INSERT INTO check_ins (attendee_id) VALUES (:attendee_id) RETURNING *"
                ),
                {"attendee_id": attendee_id},
            )
            connection.commit.assert_called_once()
            assert isinstance(check_in, CheckInEntity)
            assert check_in.check_in_id == 1
            assert check_in.created_at == "2023-10-01 12:00:00"

    def test_register_check_in_failure(self):
        with patch("src.modules.events.dao.check_in.text") as text:
            mock_connect = MagicMock(spec=ConnectionInterface)
            mock_connect.get_engine.return_value = MagicMock()
            engine = mock_connect.get_engine.return_value
            engine.connect.return_value = MagicMock()
            connection = engine.connect.return_value.__enter__.return_value
            connection.execute.return_value.first.return_value = None
            dao = CheckInDAO(connection=mock_connect)
            # Call the method
            attendee_id = "123"
            with raises(CheckInNotRegistered) as exc:
                dao.register_check_in(attendee_id)
            mock_connect.get_engine.assert_called_once()
            # Assertions
            connection.execute.assert_called_once_with(
                text(
                    "INSERT INTO check_ins (attendee_id) VALUES (:attendee_id) RETURNING *"
                ),
                {"attendee_id": attendee_id},
            )
            assert (
                str(exc.value)
                == "An error ocurred while registering the check in for the given attendee."
            )

    def test_register_check_in_integrity_error(self):
        with patch("src.modules.events.dao.check_in.text") as text:
            mock_connect = MagicMock(spec=ConnectionInterface)
            mock_connect.get_engine.return_value = MagicMock()
            engine = mock_connect.get_engine.return_value
            engine.connect.return_value = MagicMock()
            connection = engine.connect.return_value.__enter__.return_value

            def side_effect():
                raise IntegrityError("Integrity error", orig=None, params={})

            connection.execute.return_value.first.side_effect = side_effect

            dao = CheckInDAO(connection=mock_connect)
            # Call the method
            attendee_id = "123"
            with raises(CheckInNotRegistered) as exc:
                dao.register_check_in(attendee_id)
            mock_connect.get_engine.assert_called_once()
            # Assertions
            connection.execute.assert_called_once_with(
                text(
                    "INSERT INTO check_ins (attendee_id) VALUES (:attendee_id) RETURNING *"
                ),
                {"attendee_id": attendee_id},
            )
            assert str(exc.value) == "Attendee already made check-in."
