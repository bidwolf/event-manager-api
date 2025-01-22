"""
### Event DTO

This module contains Data Access Objects representation of a Event.
Classes: 

    EventDTO
"""

from dataclasses import dataclass
from datetime import datetime

from src.modules.events.exc.common import ValidationError


@dataclass
class EventDTO:

    event_id: str
    title: str
    slug: str
    created_at: datetime
    details: str | None = None
    maximum_attendees: int | None = None


@dataclass
class EventDTOWithAmount(EventDTO):
    attendee_amount: int = 0


@dataclass
class EventRegistrationDTO:
    title: str
    slug: str
    details: str | None = None
    maximum_attendees: int | None = None

    def __post_init__(self):
        self.__validate()

    def __validate_title(self):
        if not (self.title and isinstance(self.title, str)):
            raise ValidationError("The event title is missing.")
        if len(self.title) < 3:
            raise ValidationError("The event title should have at least 3 characters.")

    def __validate_slug(self):
        if not (self.slug and isinstance(self.slug, str)):
            raise ValidationError("The event slug is missing.")
        if len(self.slug) < 3:
            raise ValidationError("The event slug should have at least 3 characters.")

    def __validate_maximum_attendees(self):
        if self.maximum_attendees is not None and not isinstance(
            self.maximum_attendees, int
        ):
            raise ValidationError("'maximum attendees' should be an integer.")

    def __validate_details(self):
        if self.details is not None and not isinstance(self.details, str):
            raise ValidationError("'details' should be a string.")

    def __validate(self):
        self.__validate_title()
        self.__validate_slug()
        self.__validate_maximum_attendees()
        self.__validate_details()
