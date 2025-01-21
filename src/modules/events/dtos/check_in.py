"""
### CheckIn DTO

This module contains Data Access Objects representation of a Event CheckIn.
Classes: 

    CheckInDTO
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CheckInDTO:

    check_in_id: int
    created_at: datetime
    attendee_id: str
