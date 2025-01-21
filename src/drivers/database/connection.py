from sqlalchemy import create_engine
from src.drivers.database.types import ConnectionInterface


class DBConnection(ConnectionInterface):
    """Connection implementation for the sqlalchemy database connection"""

    def __init__(self):
        self.__connection_string = "sqlite:///instance/pass_in.db"
        self.__engine = None

    def make_connection(self):
        self.__engine = create_engine(self.__connection_string)

    def get_engine(self):
        return self.__engine

    def disconnect(self):
        if self.__engine:
            self.__engine.dispose()
            self.__engine = None


connection = DBConnection()
