from datetime import datetime
from unittest.mock import MagicMock, patch
from src.drivers.database.types import ConnectionInterface
from src.modules.events.dao.event import EventDAO
from src.modules.events.entities.event import EventEntity


class TestEventInfo:
    def setup_method(self):
        self.connection = MagicMock(spec=ConnectionInterface)
        self.query = None

    def test_event_info_not_found_returns_none(self):
        with patch("src.modules.events.dao.event.text") as text:
            self.query = text("SELECT * FROM events WHERE id =:id LIMIT 1")
            dao = EventDAO(connection=self.connection)
            event_id = "23"
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            db_connection.execute.return_value.first.return_value = None
            result = dao.get_event_info(event_id=event_id)
            db_connection.execute.return_value.first.assert_called_once()
            db_connection.execute.assert_called_once_with(self.query, {"id": event_id})
            assert result is None

    def test_event_info(self):
        with patch("src.modules.events.dao.event.text") as text:
            self.query = text("SELECT * FROM events WHERE id =:id LIMIT 1")
            dao = EventDAO(connection=self.connection)
            event_id = "23"
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            row = (
                "id",
                "title",
                "details",
                "slug",
                0,  # maximum attendees row
                datetime(2024, 1, 1),  # created_at
                0,
            )
            db_connection.execute.return_value.first.return_value = row
            result = dao.get_event_info(event_id=event_id)
            self.connection.get_engine.assert_called_once()
            self.connection.get_engine.return_value.connect.assert_called_once()
            db_connection.execute.return_value.first.assert_called_once()
            db_connection.execute.assert_called_once_with(self.query, {"id": event_id})
            assert isinstance(result, EventEntity)
            assert result.id == row[0]
            assert result.title == row[1]
            assert result.details == row[2]
            assert result.slug == row[3]
            assert result.maximum_attendees == row[4]
            assert result.created_at == row[5]

    def test_event_info_list(self):
        with patch("src.modules.events.dao.event.text") as text:
            self.query = text("SELECT * FROM events")
            dao = EventDAO(connection=self.connection)
            event_id = "23"
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            rows = [
                (
                    "id",
                    "title",
                    "details",
                    "slug",
                    0,  # maximum attendees row
                    datetime(2024, 1, 1),  # created_at
                    1,
                )
            ]
            db_connection.execute.return_value.fetchall.return_value = rows
            result = dao.get_all_events()
            db_connection.execute.return_value.fetchall.assert_called_once()
            db_connection.execute.assert_called_once_with(
                self.query,
            )
            assert result[0].id == rows[0][0]
            assert result[0].title == rows[0][1]
            assert result[0].details == rows[0][2]
            assert result[0].slug == rows[0][3]
            assert result[0].maximum_attendees == rows[0][4]
            assert result[0].created_at == rows[0][5]

    def test_event_info_list_empty(self):
        with patch("src.modules.events.dao.event.text") as text:
            query = text("SELECT * FROM events")
            dao = EventDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            rows = []
            db_connection.execute.return_value.fetchall.return_value = rows
            result = dao.get_all_events()
            db_connection.execute.return_value.fetchall.assert_called_once()
            db_connection.execute.assert_called_once_with(query)
            assert len(result) == 0
