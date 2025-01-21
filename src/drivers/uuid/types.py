"""
This module provides the inteferface of a class that is a facade
for a UUID Provider that take care of generates unique identifiers
"""

from abc import ABC, abstractmethod


class UUIDProviderInterface(ABC):
    @classmethod
    @abstractmethod
    def make_uuid(cls) -> str:
        """Generates a unique identifier"""
