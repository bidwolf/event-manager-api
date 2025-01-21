"""
### Entities

This module contains domain representations for attendees of a event.
Classes: 

    AttendeeEntity
"""

from datetime import datetime
from typing import TypedDict, Unpack
from src.drivers.uuid.driver import UUIDProvider


class AttendeeAttributes(TypedDict):
    attendee_id: str | None
    name: str
    email: str
    event_id: str
    created_at: datetime | None
    checked_in_at: datetime | None


class AttendeeEntity:
    """The event participant subscribed"""

    def __init__(self, **attendee_info: Unpack[AttendeeAttributes]):

        self.id: str = attendee_info["attendee_id"] or UUIDProvider.make_uuid()
        self.name: str = attendee_info["name"]
        self.email: str = attendee_info["email"]
        self.event_id: str = attendee_info["event_id"]
        self.created_at = attendee_info["created_at"] or datetime.now()
        self.checked_in_at = attendee_info["checked_in_at"]
