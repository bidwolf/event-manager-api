from unittest.mock import MagicMock, patch

from src.drivers.database.types import ConnectionInterface
from src.modules.events.dao.attendee import AttendeeDAO


class TestTotalParticipants:
    def setup_method(self):
        self.connection = MagicMock(spec=ConnectionInterface)
        self.query = ""

    def test_attendee_count_participants(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            self.query = text(
                """ 
                    SELECT COUNT(*) 
                    FROM attendees AS at 
                    WHERE at.event_id = :id 
                    AND at.name LIKE :query 
              """
            )
            dao = AttendeeDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            query_result = 1
            db_connection.execute.return_value.scalar.return_value = query_result
            query = ""
            result = dao.count_event_participants(event_id="1", query=query)
            db_connection.execute.return_value.scalar.assert_called_once()
            db_connection.execute.assert_called_once_with(
                self.query, {"id": "1", "query": f"%{query}%"}
            )
            assert result == 1

    def test_attendee_count_participants_is_none(self):
        with patch("src.modules.events.dao.attendee.text") as text:
            self.query = text(
                """ 
                    SELECT COUNT(*) 
                    FROM attendees AS at 
                    WHERE at.event_id = :id 
                    AND at.name LIKE :query 
              """
            )
            dao = AttendeeDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            query_result = None
            db_connection.execute.return_value.scalar.return_value = query_result
            query = ""
            result = dao.count_event_participants(event_id="1", query=query)
            db_connection.execute.return_value.scalar.assert_called_once()
            db_connection.execute.assert_called_once_with(
                self.query, {"id": "1", "query": f"%{query}%"}
            )
            assert result == 0
