from abc import ABC, abstractmethod

from src.modules.events.dtos.attendee import AttendeeDTO, AttendeeRegistrationDTO
from src.modules.events.dtos.event_credentials import EventCredentialsDTO
from src.modules.events.entities.attendee import AttendeeEntity
from src.modules.events.exc.attendee import (
    AttendeeAlreadyExistsError,
    AttendeeNotCreatedError,
    AttendeeNotFoundError,
)
from src.modules.events.exc.event import EventNotFoundError, EventSoldOutError
from src.modules.events.repositories.attendee import AttendeeRepositoryInterface
from src.modules.events.services.event import EventServiceInterface


class AttendeeServiceInterface(ABC):
    @abstractmethod
    def register_attendee_in_event(
        self, data: AttendeeRegistrationDTO
    ) -> AttendeeDTO | None:
        """Verifies the event and register the attendee in that event"""

    @abstractmethod
    def get_event_attendees(
        self, event_id: str, query: str, offset: int
    ) -> list[AttendeeDTO] | None:
        """Retrieve the attendee list registered in the given event id"""

    @abstractmethod
    def get_attendee_data(self, attendee_id: str) -> AttendeeDTO | None:
        """Retrive the attendee data with the given id"""

    @abstractmethod
    def get_attendee_event_credential(
        self, attendee_id: str
    ) -> EventCredentialsDTO | None:
        """Retrieve the event credential for the given attendee"""


class AttendeeService(AttendeeServiceInterface):
    def __init__(
        self,
        repository: AttendeeRepositoryInterface,
        event_service: EventServiceInterface,
    ):
        self.__repository = repository
        self.__event_service = event_service

    def register_attendee_in_event(self, data) -> AttendeeDTO | None:
        event_exists = self.__event_service.check_event_existence(
            event_id=data.event_id
        )
        if not event_exists:
            raise EventNotFoundError(
                "This registration failed because the given event was not Found."
            )
        attendee_already_registered = self.__event_service.check_attendee_in_event(
            attendee_email=data.email, event_id=data.event_id
        )
        if attendee_already_registered:
            raise AttendeeAlreadyExistsError("This attendee is already registered")
        has_vacancies = self.__event_service.evaluate_event_capacity(
            event_id=data.event_id
        )
        if not has_vacancies:
            raise EventSoldOutError(
                "This registration failed because the event has sold out."
            )
        new_attendee = AttendeeEntity(
            name=data.name,
            email=data.email,
            event_id=data.event_id,
            created_at=None,
            attendee_id=None,
            checked_in_at=None,
        )
        attendee_created = self.__repository.create(data=new_attendee)

        if attendee_created is None:
            raise AttendeeNotCreatedError(
                "An error ocurred while registering the attendee."
            )
        return AttendeeDTO(
            attendee_id=attendee_created.id,
            event_id=attendee_created.event_id,
            email=attendee_created.email,
            created_at=attendee_created.created_at,
            name=attendee_created.name,
            checked_in_at=None,
        )

    @staticmethod
    def __convert_entity_to_dto(attendee: AttendeeEntity) -> AttendeeDTO:
        return AttendeeDTO(
            attendee_id=attendee.id,
            name=attendee.name,
            email=attendee.email,
            event_id=attendee.event_id,
            created_at=attendee.created_at,
            checked_in_at=attendee.checked_in_at,
        )

    def get_event_attendees(self, event_id, query, offset):
        event_exists = self.__event_service.check_event_existence(event_id=event_id)
        if not event_exists:
            raise EventNotFoundError("The given event not exists.")
        entity_participants = self.__repository.get_event_participants(
            event_id=event_id, offset=offset, query=query
        )
        dto_participants = [
            self.__convert_entity_to_dto(attendee=attendee)
            for attendee in entity_participants
        ]
        return dto_participants

    def get_attendee_data(self, attendee_id) -> AttendeeDTO | None:
        attendee = self.__repository.get_attendee_by_id(attendee_id=attendee_id)
        if attendee is None:
            raise AttendeeNotFoundError("Attendee not found.")
        return AttendeeDTO(
            attendee_id=attendee.id,
            checked_in_at=attendee.checked_in_at,
            created_at=attendee.created_at,
            email=attendee.email,
            event_id=attendee.event_id,
            name=attendee.name,
        )

    def get_attendee_event_credential(self, attendee_id):
        attendee = self.__repository.get_attendee_by_id(attendee_id=attendee_id)
        if attendee is None:
            raise AttendeeNotFoundError("Attendee not found.")
        event_data = self.__event_service.get_event_data(event_id=attendee.event_id)
        if event_data is None:
            raise EventNotFoundError("The registered event was not found.")
        return EventCredentialsDTO(
            event_title=event_data.title,
            email=attendee.email,
            name=attendee.name,
        )
