import pytest
from src.drivers.database.connection import DBConnection


@pytest.fixture(name="connection")
def get_connection():
    """fixture for integration tests with pytest"""
    connection = DBConnection()
    connection.make_connection()
    yield connection
    connection.disconnect()
