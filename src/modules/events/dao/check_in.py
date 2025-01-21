from abc import ABC, abstractmethod
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from src.drivers.database.types import ConnectionInterface
from src.modules.events.entities.check_in import CheckInEntity
from src.modules.events.exc.check_in import CheckInNotRegistered


class CheckInDaoInterface(ABC):
    @abstractmethod
    def register_check_in(self, attendee_id: str) -> CheckInEntity | None:
        """Realize the check in for the attendee in their event"""


class CheckInDAO(CheckInDaoInterface):
    def __init__(self, connection: ConnectionInterface):
        self.__connection = connection

    def register_check_in(self, attendee_id) -> CheckInEntity | None:
        engine = self.__connection.get_engine()
        with engine.connect() as connection:
            try:
                register_check_in_sql = text(
                    "INSERT INTO check_ins (attendee_id) VALUES (:attendee_id) RETURNING *"
                )
                result = connection.execute(
                    register_check_in_sql, {"attendee_id": attendee_id}
                )
                check_in_data = result.first()
                if check_in_data is None:
                    raise CheckInNotRegistered(
                        "An error ocurred while registering the check in for the given attendee."
                    )
                connection.commit()
                return CheckInEntity(
                    check_in_id=check_in_data[0],
                    created_at=check_in_data[1],
                    attendee_id=check_in_data[2],
                )
            except IntegrityError as exc:
                raise CheckInNotRegistered("Attendee already made check-in.") from exc
