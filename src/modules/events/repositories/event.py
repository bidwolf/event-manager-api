from abc import ABC, abstractmethod
from src.modules.events.dao.event import EventDaoInterface
from src.modules.events.dtos.event import EventDTOWithAmount
from src.modules.events.entities.event import EventEntity


class EventRepositoryInterface(ABC):
    """Represent Layer at top a collection"""

    @abstractmethod
    def create(self, data: EventEntity) -> EventEntity | None:
        """Create a new event"""

    @abstractmethod
    def get_event_by_id(self, event_id: str) -> EventDTOWithAmount | None:
        """Retrieve a event information with the given id"""

    @abstractmethod
    def check_event_existence(self, event_id: str) -> bool:
        """Checks the existence of a event with the given id"""

    @abstractmethod
    def check_event_capacity(self, event_id: str) -> bool:
        """Check if the event has vacancies"""

    @abstractmethod
    def check_participant_existence(self, attendee_email: str, event_id: str) -> bool:
        """Check if the participant is registered in the event"""

    @abstractmethod
    def load_events_list(self, offset: int, query: str) -> list[EventEntity]:
        """Retrieve all events available"""


class EventRepository(EventRepositoryInterface):
    def __init__(self, dao: EventDaoInterface):
        self.__event_dao = dao

    def create(self, data) -> EventEntity | None:
        return self.__event_dao.create_event(event_data=data)

    def get_event_by_id(self, event_id: str):
        return self.__event_dao.get_event_info(event_id=event_id)

    def check_event_existence(self, event_id: str) -> bool:
        return self.__event_dao.check_event_exists(event_id=event_id)

    def check_event_capacity(self, event_id):
        return self.__event_dao.check_event_has_vacancies(event_id=event_id)

    def check_participant_existence(self, attendee_email: str, event_id: str) -> bool:
        return self.__event_dao.check_attendee_in_event(
            attendee_email=attendee_email, event_id=event_id
        )

    def load_events_list(self, offset, query):
        return self.__event_dao.retrieve_events(offset=offset, query=query)
