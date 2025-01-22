"""
This module is responsible to contain all business logic related to the event.
"""

from abc import ABC, abstractmethod

from src.modules.events.dtos.event import (
    EventDTO,
    EventDTOWithAmount,
    EventRegistrationDTO,
)
from src.modules.events.entities.event import EventEntity

from src.modules.events.exc.event import (
    EventAlreadyExistsError,
    EventNotFoundError,
    EventNotCreatedError,
)

from src.modules.events.repositories.event import EventRepositoryInterface


class EventServiceInterface(ABC):
    @abstractmethod
    def create_event(self, data: EventRegistrationDTO) -> EventDTO | None:
        """Create a event"""

    @abstractmethod
    def get_event_data(self, event_id: str) -> EventDTOWithAmount | None:
        """Retrieve the event data with the given id"""

    @abstractmethod
    def check_event_existence(self, event_id: str) -> bool:
        """Check if the event with the given id exists"""

    @abstractmethod
    def check_attendee_in_event(self, attendee_email: str, event_id: str) -> bool:
        """Check if the attendee is registered in the event"""

    @abstractmethod
    def evaluate_event_capacity(self, event_id: str) -> bool:
        """Evaluate if the event with the given id has available vacancies"""

    @abstractmethod
    def list_events(self, offset: int, query: str) -> list[EventDTO]:
        """Retrieve the first 10 events ordered by the creation Date"""


class EventService(EventServiceInterface):
    def __init__(self, repository: EventRepositoryInterface):
        self.__repository = repository

    def create_event(self, data: EventRegistrationDTO) -> EventDTO | None:
        new_event = EventEntity(
            title=data.title,
            slug=data.slug,
            details=data.details,
            maximum_attendees=data.maximum_attendees,
            id=None,
            created_at=None,
        )
        event_exists = self.__repository.check_event_existence(event_id=new_event.id)
        if event_exists:
            raise EventAlreadyExistsError("This event is already registered.")
        created_entity = self.__repository.create(data=new_event)
        if created_entity is None:
            raise EventNotCreatedError("An error ocurred while creating the event.")

        return EventDTO(
            title=created_entity.title,
            details=created_entity.details,
            event_id=created_entity.id,
            slug=created_entity.slug,
            maximum_attendees=created_entity.maximum_attendees,
            created_at=created_entity.created_at,
        )

    def get_event_data(self, event_id) -> EventDTOWithAmount | None:
        return self.__repository.get_event_by_id(event_id=event_id)

    def check_event_existence(self, event_id):
        return self.__repository.check_event_existence(event_id=event_id)

    def evaluate_event_capacity(self, event_id):
        return self.__repository.check_event_capacity(event_id=event_id)

    def check_attendee_in_event(self, attendee_email, event_id):
        return self.__repository.check_participant_existence(
            attendee_email=attendee_email, event_id=event_id
        )

    def __from_entity_to_dto(self, entity: EventEntity) -> EventDTO:
        return EventDTO(
            title=entity.title,
            details=entity.details,
            event_id=entity.id,
            slug=entity.slug,
            maximum_attendees=entity.maximum_attendees,
            created_at=entity.created_at,
        )

    def list_events(self, offset, query):
        event_list = self.__repository.load_events_list(offset=offset, query=query)
        return [self.__from_entity_to_dto(event) for event in event_list]
