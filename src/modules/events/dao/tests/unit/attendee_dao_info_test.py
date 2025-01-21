from datetime import datetime
from unittest.mock import MagicMock, patch
from src.drivers.database.types import ConnectionInterface
from src.modules.events.dao.attendee import AttendeeDAO
from src.modules.events.entities.attendee import AttendeeEntity


class TestAttendeeInfo:
    def setup_method(self):
        self.connection = MagicMock(spec=ConnectionInterface)
        self.query = None

    def test_attendee_info_not_found_returns_none(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            self.query = text(
                """
            SELECT
                at.id AS attendee_id,
                at.name AS attendee_name,
                at.email AS attendee_email,
                at.created_at AS attendee_registered_at,
                at.event_id,
                chk.created_at AS checked_in_at
            FROM attendees AS at
            LEFT JOIN check_ins AS chk
            ON chk.attendee_id = at.id
            WHERE at.id = :id;
            """
            )
            dao = AttendeeDAO(connection=self.connection)
            attendee_id = "23"
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            db_connection.execute.return_value.first.return_value = None
            result = dao.get_attendee_data(attendee_id=attendee_id)
            db_connection.execute.return_value.first.assert_called_once()
            db_connection.execute.assert_called_once_with(
                self.query, {"id": attendee_id}
            )
            assert result is None

    def test_attendee_info(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            self.query = text(
                """
            SELECT
                at.id AS attendee_id,
                at.name AS attendee_name,
                at.email AS attendee_email,
                at.created_at AS attendee_registered_at,
                at.event_id,
                chk.created_at AS checked_in_at
            FROM attendees AS at
            LEFT JOIN check_ins AS chk
            ON chk.attendee_id = at.id
            WHERE at.id = :id;
            """
            )
            dao = AttendeeDAO(connection=self.connection)
            attendee_id = "23"
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            row = (
                "attendee_id",
                "name",
                "email@email.com",
                datetime(2024, 1, 1),  # created_at
                "event_id",
                datetime(2024, 1, 1),  # checked_in_at
            )
            db_connection.execute.return_value.first.return_value = row
            result = dao.get_attendee_data(attendee_id=attendee_id)
            self.connection.get_engine.assert_called_once()
            self.connection.get_engine.return_value.connect.assert_called_once()
            db_connection.execute.return_value.first.assert_called_once()
            db_connection.execute.assert_called_once_with(
                self.query, {"id": attendee_id}
            )
            assert isinstance(result, AttendeeEntity)
            assert result.id == row[0]
            assert result.name == row[1]
            assert result.email == row[2]
            assert result.created_at == row[3]
            assert result.event_id == row[4]
            assert result.checked_in_at == row[5]

    def test_attendee_info_list(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            self.query = text(
                """
                SELECT
                    at.id AS attendee_id,
                    at.name AS attendee_name,
                    at.email AS attendee_email,
                    at.created_at AS attendee_registered_at,
                    at.event_id,
                    chk.created_at AS checked_in_at
                FROM events AS ev
                LEFT JOIN attendees AS at
                ON at.event_id=ev.id
                LEFT JOIN check_ins AS chk
                ON chk.attendee_id = at.id
                WHERE ev.id = :id
                ORDER BY at.name DESC;
            """
            )
            dao = AttendeeDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            rows = [
                (
                    "attendee_id",
                    "name",
                    "email@email.com",
                    datetime(2024, 1, 1),  # created_at
                    "event_id",
                    datetime(2024, 1, 1),  # checked_in_at
                )
            ]
            db_connection.execute.return_value.fetchall.return_value = rows
            result = dao.get_event_participants(event_id="1")
            db_connection.execute.return_value.fetchall.assert_called_once()
            db_connection.execute.assert_called_once_with(self.query, {"id": "1"})
            assert result[0].id == rows[0][0]
            assert result[0].name == rows[0][1]
            assert result[0].email == rows[0][2]
            assert result[0].created_at == rows[0][3]
            assert result[0].event_id == rows[0][4]
            assert result[0].checked_in_at == rows[0][5]

    def test_attendee_info_list_empty(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            self.query = text(
                """
                SELECT
                    at.id AS attendee_id,
                    at.name AS attendee_name,
                    at.email AS attendee_email,
                    at.created_at AS attendee_registered_at,
                    at.event_id,
                    chk.created_at AS checked_in_at
                FROM events AS ev
                LEFT JOIN attendees AS at
                ON at.event_id=ev.id
                LEFT JOIN check_ins AS chk
                ON chk.attendee_id = at.id
                WHERE ev.id = :id
                ORDER BY at.name DESC;
            """
            )
            dao = AttendeeDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            rows = []
            db_connection.execute.return_value.fetchall.return_value = rows
            result = dao.get_event_participants(event_id="1")
            db_connection.execute.return_value.fetchall.assert_called_once()
            db_connection.execute.assert_called_once_with(self.query, {"id": "1"})
            assert len(result) == 0
