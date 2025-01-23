from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import Row, text
from sqlalchemy.exc import IntegrityError
from src.drivers.database.types import ConnectionInterface
from src.modules.events.entities.attendee import AttendeeEntity
from src.modules.events.exc.attendee import AttendeeAlreadyExistsError


class AttendeeDaoInterface(ABC):

    @abstractmethod
    def get_event_participants(
        self, event_id: str, query: str, offset: int
    ) -> list[AttendeeEntity]:
        """Retrieve registered attendees for the event with the given Id"""

    @abstractmethod
    def register_participant(self, attendee: AttendeeEntity) -> AttendeeEntity | None:
        """Register a attendee in a event"""

    @abstractmethod
    def get_attendee_data(self, attendee_id: str) -> AttendeeEntity | None:
        """Retrieve data related to the given attendee id"""


class AttendeeDAO(AttendeeDaoInterface):
    def __init__(self, connection: ConnectionInterface):
        self.__connection = connection

    def __row_to_entity(self, row: Row[Any]) -> AttendeeEntity:
        return AttendeeEntity(
            attendee_id=row[0],
            name=row[1],
            email=row[2],
            created_at=row[3],
            event_id=row[4],
            checked_in_at=row[5],
        )

    def get_attendee_data(self, attendee_id):
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            get_attendee_data_sql = text(
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
            result = connection.execute(get_attendee_data_sql, {"id": attendee_id})
            row = result.first()
            if row is None:
                return None
            return self.__row_to_entity(row=row)

    def get_event_participants(self, event_id, query="", offset=0):
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            get_attendee_data_sql = text(
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
                WHERE ev.id = :id AND at.name LIKE :query
                ORDER BY at.name DESC
                LIMIT 10
                OFFSET 10 * :offset
            """
            )
            result = connection.execute(
                get_attendee_data_sql,
                {"id": event_id, "query": f"%{query}%", "offset": offset},
            )
            all_rows = result.fetchall()
            if len(all_rows) == 0:
                return []
            return [self.__row_to_entity(row=row) for row in all_rows]

    def register_participant(self, attendee) -> AttendeeEntity | None:
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            try:
                sql_query = text(
                    """
                    INSERT INTO attendees (id,name,email,event_id,created_at)
                    VALUES(:attendee_id,:name,:email,:event_id,:created_at)
                    """
                )
                result = connection.execute(
                    sql_query,
                    {
                        "attendee_id": attendee.id,
                        "name": attendee.name,
                        "email": attendee.email,
                        "event_id": attendee.event_id,
                        "created_at": attendee.created_at,
                    },
                )
                connection.commit()
                return attendee
            except IntegrityError as exc:
                raise AttendeeAlreadyExistsError(
                    "An attendee with the given email is already registered in this event."
                ) from exc
