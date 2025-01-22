"""
This module is responsible to contain all business logic related to the event.
"""

from abc import ABC, abstractmethod

from src.modules.events.dtos.event import EventDTO, EventRegistrationDTO
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
    def get_event_data(self, event_id: str) -> EventDTO | None:
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

    def get_event_data(self, event_id) -> EventDTO | None:

        event_data = self.__repository.get_event_by_id(event_id=event_id)
        if not event_data:
            raise EventNotFoundError("Event not found.")
        return EventDTO(
            title=event_data.title,
            details=event_data.details,
            event_id=event_data.id,
            slug=event_data.slug,
            maximum_attendees=event_data.maximum_attendees,
            created_at=event_data.created_at,
            attendees_amount=event_data.attendees_amount,
        )

    def check_event_existence(self, event_id):
        return self.__repository.check_event_existence(event_id=event_id)

    def evaluate_event_capacity(self, event_id):
        return self.__repository.check_event_capacity(event_id=event_id)

    def check_attendee_in_event(self, attendee_email, event_id):
        return self.__repository.check_participant_existence(
            attendee_email=attendee_email, event_id=event_id
        )
