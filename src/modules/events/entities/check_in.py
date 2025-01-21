from datetime import datetime
from typing import TypedDict, Unpack


class CheckInAttributes(TypedDict):
    check_in_id: str
    attendee_id: str
    created_at: datetime


class CheckInEntity:
    """The Check in for a attendee in a event"""

    def __init__(self, **check_in: Unpack[CheckInAttributes]):
        self.check_in_id = check_in["check_in_id"]
        self.created_at = check_in["created_at"]
        self.attendee_id = check_in["attendee_id"]

    def emit_credential(self) -> None:
        """Creates a QR Code passport that can be used to enter in the registered Event"""

    def make_check_in(self, credential: str):
        """Validate the given credential given credential and check in the attendee in the event"""
