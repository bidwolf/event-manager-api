"""
This module contains a facade for the uuid library that is going to be used
to generate unique identifiers for the entire appliation
"""

import uuid
from src.drivers.uuid.types import UUIDProviderInterface


class UUIDProvider(UUIDProviderInterface):
    """
    This class is responsible to provide methods to create
    unique identifiers to the application.
    """

    @classmethod
    def make_uuid(cls):
        return str(uuid.uuid4())
