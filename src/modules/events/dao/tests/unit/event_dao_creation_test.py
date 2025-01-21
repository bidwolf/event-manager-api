from datetime import datetime
from unittest.mock import MagicMock, patch
from pytest import raises
from sqlalchemy.exc import IntegrityError
from src.drivers.database.types import ConnectionInterface
from src.modules.events.dao.event import EventDAO
from src.modules.events.entities.event import EventEntity
from src.modules.events.exc.event import EventAlreadyExistsError


class TestEventCreationDAO:
    def setup_method(self):
        self.connection = MagicMock(spec=ConnectionInterface)

    def test_register_event(self):
        with patch("src.modules.events.dao.event.text") as text:

            dao = EventDAO(connection=self.connection)
            event_data = EventEntity(
                created_at=datetime.now(),
                details="any",
                maximum_attendees=1,
                slug="any",
                title="any",
                id=None,
            )
            result = dao.create_event(event_data=event_data)
            self.connection.get_engine.assert_called_once()
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            db_connection.execute.assert_called_once_with(
                text(
                    "INSERT INTO events (id,title,details,slug,maximum_attendees,created_at)"
                    " VALUES(:id,:title,:details,:slug,:maximum_attendees,:created_at)"
                ),
                {
                    "id": event_data.id,
                    "title": event_data.title,
                    "details": event_data.details,
                    "slug": event_data.slug,
                    "maximum_attendees": event_data.maximum_attendees,
                    "created_at": event_data.created_at,
                },
            )
            db_connection.commit.assert_called_once()

            assert result == event_data

    def test_register_event_integrity_error(self):
        with patch("src.modules.events.dao.event.text") as text:

            dao = EventDAO(connection=self.connection)
            event_data = EventEntity(
                created_at=datetime.now(),
                details="any",
                maximum_attendees=1,
                slug="any",
                title="any",
                id=None,
            )

            def side_effect():
                raise IntegrityError("Integrity error", orig=None, params={})

            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            db_connection.commit.side_effect = side_effect
            with raises(EventAlreadyExistsError) as exc:
                dao.create_event(event_data=event_data)
            self.connection.get_engine.assert_called_once()

            db_connection.execute.assert_called_once_with(
                text(
                    "INSERT INTO events (id,title,details,slug,maximum_attendees,created_at)"
                    " VALUES(:id,:title,:details,:slug,:maximum_attendees,:created_at)"
                ),
                {
                    "id": event_data.id,
                    "title": event_data.title,
                    "details": event_data.details,
                    "slug": event_data.slug,
                    "maximum_attendees": event_data.maximum_attendees,
                    "created_at": event_data.created_at,
                },
            )
            db_connection.commit.assert_called_once()
            assert str(exc.value) == "An event with this slug already exists."
