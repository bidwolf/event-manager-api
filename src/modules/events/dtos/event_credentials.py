from dataclasses import dataclass


@dataclass
class EventCredentialsDTO:
    """Represents the data related to a attendee and a event to make an event credential"""

    event_title: str
    name: str
    email: str
