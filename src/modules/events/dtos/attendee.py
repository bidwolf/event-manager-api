"""
### Event DTO

This module contains Data Access Objects representations for a Attendee of a Events.
Classes: 

    AttendeeDTO
"""

from dataclasses import dataclass
from datetime import datetime

from src.modules.events.exc.common import ValidationError
from src.utils.validators import email_validator, name_validator


@dataclass
class AttendeeDTO:
    attendee_id: str
    name: str
    email: str
    event_id: str
    created_at: datetime
    checked_in_at: datetime | None


@dataclass
class AttendeeRegistrationDTO:
    name: str
    email: str
    event_id: str

    def __post_init__(self):
        self.__validate_event_id()
        self.__validate_email()
        self.__validate_name()

    def __validate_event_id(self):

        if not isinstance(self.event_id, str):
            raise ValidationError("The event id should be a string.")

    def __validate_email(self):
        valid_email = email_validator(self.email)
        if not valid_email:
            raise ValidationError("The email is invalid.")

    def __validate_name(self):
        valid_name = name_validator(self.name)
        if not isinstance(self.name, str):
            raise ValidationError("The name should be a string.")
        if not valid_name:
            raise ValidationError("The name is invalid.")
