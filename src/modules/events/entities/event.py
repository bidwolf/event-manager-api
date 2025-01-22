"""
### Entities

This module contains domain representations of events.
Classes: 

    EventEntity
"""

from datetime import datetime
from typing import TypedDict, Unpack

from src.drivers.uuid.driver import UUIDProvider


class EventAttributes(TypedDict):
    """Event Arguments"""

    id: str | None
    title: str
    slug: str
    details: str | None
    maximum_attendees: int | None
    created_at: datetime | None


class EventEntity:
    """The event for the pass in"""

    def __init__(self, **event: Unpack[EventAttributes]):
        self.id = event.get("id") or UUIDProvider.make_uuid()
        self.title = event["title"]
        self.slug = event["slug"]
        self.details = event["details"]
        self.maximum_attendees = event["maximum_attendees"]
        self.created_at = event.get("created_at") or datetime.now()
