from dataclasses import dataclass
from datetime import datetime


@dataclass
class EventCredentialsDTO:
    """Represents the data related to a attendee and a event to make an event credential"""

    event_title: str
    event_details: str
    event_slug: str
    event_id: str
    participant_id: str
    participant_name: str
    participant_email: str
    registered_at: datetime
