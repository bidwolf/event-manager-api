from abc import ABC, abstractmethod

from src.modules.events.dtos.check_in import CheckInDTO
from src.modules.events.entities.check_in import CheckInEntity
from src.modules.events.exc.attendee import AttendeeNotFoundError
from src.modules.events.exc.check_in import AlreadyCheckedInError, CheckInNotRegistered
from src.modules.events.repositories.check_in import CheckInRepositoryInterface
from src.modules.events.services.attendee import AttendeeServiceInterface


class CheckInServiceInterface(ABC):
    @abstractmethod
    def make_event_check_in(self, attendee_id: str) -> CheckInDTO | None:
        """Check-in the Attendee with the given id"""


class CheckInService(CheckInServiceInterface):
    def __init__(
        self,
        repository: CheckInRepositoryInterface,
        attendee_service: AttendeeServiceInterface,
    ):
        self.__repository = repository
        self.__attendee_service = attendee_service

    def make_event_check_in(self, attendee_id) -> CheckInDTO | None:
        attendee = self.__attendee_service.get_attendee_data(attendee_id=attendee_id)
        if not attendee:
            raise AttendeeNotFoundError(
                "The given attendee is not registered in any event."
            )
        if attendee.checked_in_at is not None:
            raise AlreadyCheckedInError("Attendee has already made a check in.")
        check_in_data = self.__repository.register_check_in(attendee_id=attendee_id)
        if not check_in_data:
            raise CheckInNotRegistered("An error ocurred while making the checkin")
        return check_in_data
