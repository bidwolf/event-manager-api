from datetime import datetime
from unittest.mock import MagicMock, patch
from pytest import raises
from sqlalchemy.exc import IntegrityError
from src.drivers.database.types import ConnectionInterface
from src.modules.events.dao.attendee import AttendeeDAO
from src.modules.events.entities.attendee import AttendeeEntity
from src.modules.events.exc.attendee import AttendeeAlreadyExistsError


class TestEventCreationDAO:
    def setup_method(self):
        self.connection = MagicMock(spec=ConnectionInterface)

    def test_register_attendee(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            sql_query = text(
                """
                    INSERT INTO attendees (id,name,email,event_id,created_at)
                    VALUES(:attendee_id,:name,:email,:event_id,:created_at)
                    """
            )
            dao = AttendeeDAO(connection=self.connection)
            attendee = AttendeeEntity(
                created_at=datetime.now(),
                checked_in_at=None,
                event_id="1",
                email="any@gmail.com",
                name="anyname",
                attendee_id=None,
            )
            result = dao.register_participant(attendee=attendee)
            self.connection.get_engine.assert_called_once()
            self.connection.get_engine.assert_called_once()
            self.connection.get_engine.return_value.connect.assert_called_once()
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            db_connection.execute.assert_called_once_with(
                sql_query,
                {
                    "attendee_id": attendee.id,
                    "name": attendee.name,
                    "email": attendee.email,
                    "event_id": attendee.event_id,
                    "created_at": attendee.created_at,
                },
            )
            db_connection.commit.assert_called_once()

            assert result == attendee

    def test_register_attendee_integrity_error(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            sql_query = text(
                """
                    INSERT INTO attendees (id,name,email,event_id,created_at)
                    VALUES(:attendee_id,:name,:email,:event_id,:created_at)
                    """
            )
            dao = AttendeeDAO(connection=self.connection)
            attendee = AttendeeEntity(
                created_at=datetime.now(),
                checked_in_at=None,
                event_id="1",
                email="any@gmail.com",
                name="anytest",
                attendee_id=None,
            )

            def side_effect():
                raise IntegrityError("Integrity error", orig=None, params={})

            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            db_connection.commit.side_effect = side_effect
            with raises(AttendeeAlreadyExistsError) as exc:
                dao.register_participant(attendee=attendee)
            self.connection.get_engine.assert_called_once()

            db_connection.execute.assert_called_once_with(
                sql_query,
                {
                    "attendee_id": attendee.id,
                    "name": attendee.name,
                    "email": attendee.email,
                    "event_id": attendee.event_id,
                    "created_at": attendee.created_at,
                },
            )
            db_connection.commit.assert_called_once()
            assert (
                str(exc.value)
                == "An attendee with the given email is already registered in this event."
            )
