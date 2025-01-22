from abc import ABC, abstractmethod
from typing import Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Row, text

from src.drivers.database.types import ConnectionInterface
from src.modules.events.dtos.event import EventDTOWithAmount
from src.modules.events.entities.event import EventEntity
from src.modules.events.exc.event import EventAlreadyExistsError


class EventDaoInterface(ABC):
    @abstractmethod
    def get_event_info(self, event_id: str) -> EventDTOWithAmount | None:
        """Retrieves data about an event without participants"""

    @abstractmethod
    def retrieve_events(self, offset: int, query: str) -> list[EventEntity]:
        """Retrieves all valid Events from the database"""

    @abstractmethod
    def create_event(self, event_data: EventEntity) -> EventEntity | None:
        """Creates a new event using the given event_data"""

    @abstractmethod
    def check_event_exists(self, event_id=str) -> bool:
        """Checks for the existence of the event"""

    @abstractmethod
    def check_event_has_vacancies(self, event_id=str) -> bool:
        """Check if the event has vacancies for new attendees"""

    @abstractmethod
    def check_attendee_in_event(self, attendee_email: str, event_id: str) -> bool:
        """Check if the attendee is registered in the given event"""


class EventDAO(EventDaoInterface):
    def __init__(self, connection: ConnectionInterface):
        self.__connection = connection

    def __row_to_event_entity(self, row: Row[Any]) -> EventEntity:

        return EventEntity(
            id=row[0],
            title=row[1],
            details=row[2],
            slug=row[3],
            maximum_attendees=row[4],
            created_at=row[5],
        )

    def get_event_info(self, event_id) -> EventDTOWithAmount | None:
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT
                    ev.*,
                    COUNT(at.id) AS attendees_amount
                    FROM attendees AS at
                    LEFT JOIN events AS ev
                    ON at.event_id = ev.id
                    WHERE ev.id = :id
                    GROUP BY ev.id
                     """
                ),
                {"id": event_id},
            )
            row = result.first()
            if row is None:
                return None
            return EventDTOWithAmount(
                event_id=row[0],
                title=row[1],
                details=row[2],
                slug=row[3],
                maximum_attendees=row[4],
                created_at=row[5],
                attendee_amount=row[6],
            )

    def create_event(self, event_data) -> EventEntity | None:
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            try:
                query_sql = text(
                    "INSERT INTO events (id,title,details,slug,maximum_attendees,created_at)"
                    " VALUES(:id,:title,:details,:slug,:maximum_attendees,:created_at)"
                )
                connection.execute(
                    query_sql,
                    {
                        "id": event_data.id,
                        "title": event_data.title,
                        "details": event_data.details,
                        "slug": event_data.slug,
                        "maximum_attendees": event_data.maximum_attendees,
                        "created_at": event_data.created_at,
                    },
                )
                connection.commit()
                return event_data
            except IntegrityError as exc:
                print(exc)
                raise EventAlreadyExistsError(
                    "An event with this slug already exists."
                ) from exc

    def retrieve_events(self, offset: int = 0, query: str = "") -> list[EventEntity]:
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT * FROM events
                    WHERE events.title LIKE :query
                    ORDER BY events.created_at DESC
                    LIMIT 10
                    OFFSET 10 * :offset
                    """
                ),
                {"offset": offset, "query": f"%{query}%"},
            )
            rows = result.fetchall()
            if len(rows) == 0:
                return []
            events = [self.__row_to_event_entity(row=event_row) for event_row in rows]
            return events

    def check_event_has_vacancies(self, event_id=str):
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
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
            result = connection.execute(has_vacancy_query, {"id": event_id})
            return bool(result.scalar())

    def check_attendee_in_event(self, attendee_email, event_id):
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            check_event_existence_query = text(
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
            result = connection.execute(
                check_event_existence_query, {"id": event_id, "email": attendee_email}
            )
            return bool(result.scalar())

    def check_event_exists(self, event_id=str):
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            check_event_existence_query = text(
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
            result = connection.execute(check_event_existence_query, {"id": event_id})
            return bool(result.scalar())
