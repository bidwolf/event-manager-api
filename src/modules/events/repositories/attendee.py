from abc import ABC, abstractmethod
from src.modules.events.dao.attendee import AttendeeDaoInterface
from src.modules.events.entities.attendee import AttendeeEntity


class AttendeeRepositoryInterface(ABC):
    @abstractmethod
    def create(self, data: AttendeeEntity) -> AttendeeEntity | None:
        """Create a attendee for the event"""

    @abstractmethod
    def get_event_participants(
        self, event_id: str, query: str, offset: int
    ) -> list[AttendeeEntity]:
        """Retrive a list of participants of the given event"""

    @abstractmethod
    def get_attendee_by_id(self, attendee_id: str) -> AttendeeEntity | None:
        """Retrieve the data of the given attendee_id"""


class AttendeeRepository(AttendeeRepositoryInterface):
    def __init__(self, dao: AttendeeDaoInterface):
        self.__dao = dao

    def create(self, data):
        return self.__dao.register_participant(attendee=data)

    def get_event_participants(self, event_id, query, offset):
        return self.__dao.get_event_participants(
            event_id=event_id, query=query, offset=offset
        )

    def get_attendee_by_id(self, attendee_id):
        return self.__dao.get_attendee_data(attendee_id=attendee_id)
