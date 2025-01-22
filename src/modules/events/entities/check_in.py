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
