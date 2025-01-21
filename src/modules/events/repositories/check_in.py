from abc import ABC, abstractmethod

from src.modules.events.dao.check_in import CheckInDaoInterface
from src.modules.events.dtos.check_in import CheckInDTO


class CheckInRepositoryInterface(ABC):
    @abstractmethod
    def register_check_in(self, attendee_id: str) -> CheckInDTO | None:
        """Register the Attendee check-in in the Event"""


class CheckInRepository(CheckInRepositoryInterface):
    def __init__(self, dao: CheckInDaoInterface):
        self.__dao = dao

    def register_check_in(self, attendee_id: str):
        return self.__dao.register_check_in(attendee_id=attendee_id)
