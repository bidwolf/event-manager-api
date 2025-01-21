from unittest.mock import MagicMock, patch
from src.drivers.database.types import ConnectionInterface
from src.modules.events.dao.event import EventDAO


class TestEventChecks:
    def setup_method(self):
        self.connection = MagicMock(spec=ConnectionInterface)

    def test_event_check_vacation(self):
        with patch("src.modules.events.dao.event.text") as text:

            dao = EventDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            event_id = "1"
            has_vacancy_query = text(
                """
                SELECT CASE 
                WHEN (
                    SELECT ev.maximum_attendees
                    FROM events as ev
                    WHERE ev.id =  :id
                ) is NULL 
                    THEN CAST (1 AS BIT)
                WHEN (
                    SELECT COUNT(*) 
                    FROM attendees AS at
                    WHERE at.event_id = :id
                ) < (
                    SELECT ev.maximum_attendees
                    FROM events AS ev
                    WHERE ev.id = :id
                )
                THEN CAST(1 AS BIT)
                ELSE CAST(0 AS BIT) END;

            """
            )
            db_connection.execute.return_value.scalar.return_value = True
            has_vacancies = dao.check_event_has_vacancies(event_id=event_id)

            self.connection.get_engine.assert_called_once()
            db_connection.execute.assert_called_once_with(
                has_vacancy_query, {"id": event_id}
            )
            db_connection.execute.return_value.scalar.assert_called_once()
            assert has_vacancies is True
            db_connection.execute.return_value.scalar.return_value = False
            new_check = dao.check_event_has_vacancies(event_id=event_id)
            assert new_check is False

    def test_event_check_existence(self):
        with patch("src.modules.events.dao.event.text") as text:

            dao = EventDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            event_id = "1"
            has_vacancy_query = text(
                """
                SELECT
                CASE WHEN EXISTS(
                    SELECT events.id 
                    FROM events 
                    WHERE events.id = :id
                ) 
                THEN CAST(1 AS BIT)
                ELSE CAST (0 AS BIT) END;
            """
            )
            db_connection.execute.return_value.scalar.return_value = True
            has_vacancies = dao.check_event_exists(event_id=event_id)

            self.connection.get_engine.assert_called_once()
            db_connection.execute.assert_called_once_with(
                has_vacancy_query, {"id": event_id}
            )
            db_connection.execute.return_value.scalar.assert_called_once()
            assert has_vacancies is True
            db_connection.execute.return_value.scalar.return_value = False
            new_check = dao.check_event_exists(event_id=event_id)
            assert new_check is False

    def test_event_check_attendee_in_event(self):
        with patch("src.modules.events.dao.event.text") as text:

            dao = EventDAO(connection=self.connection)
            db_connection = (
                self.connection.get_engine.return_value.connect.return_value.__enter__.return_value
            )
            event_id = "1"
            attendee_email = "test@gmail.com"
            has_vacancy_query = text(
                """
                SELECT
                    CASE WHEN EXISTS(
                        SELECT at.event_id
                        FROM attendees AS at
                        JOIN events AS ev
                        ON at.event_id = ev.id
                        WHERE at.event_id = :id
                        AND at.email = :email
                    )
                    THEN CAST(1 AS BIT)
                    ELSE CAST (0 AS BIT) END;
            """
            )
            db_connection.execute.return_value.scalar.return_value = True
            has_vacancies = dao.check_attendee_in_event(
                event_id=event_id, attendee_email=attendee_email
            )

            self.connection.get_engine.assert_called_once()
            db_connection.execute.assert_called_once_with(
                has_vacancy_query, {"id": event_id, "email": attendee_email}
            )
            db_connection.execute.return_value.scalar.assert_called_once()
            assert has_vacancies is True
            db_connection.execute.return_value.scalar.return_value = False
            new_check = dao.check_attendee_in_event(
                event_id=event_id, attendee_email=attendee_email
            )
            assert new_check is False
