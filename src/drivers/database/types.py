from abc import ABC, abstractmethod

from sqlalchemy import Engine


class ConnectionInterface(ABC):
    """Facade for sqlalchemy database connection"""

    @abstractmethod
    def make_connection(self):
        """This method will start a connection with the database"""

    @abstractmethod
    def disconnect(self):
        """This method will disconnect from the database"""

    @abstractmethod
    def get_engine(self) -> Engine:
        """This method will send the engine used to make sql operations"""
