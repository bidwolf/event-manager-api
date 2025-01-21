class EventAlreadyExistsError(Exception):
    def __init__(self, message: str):
        """Event already registered"""
        super().__init__(message)


class EventNotFoundError(Exception):
    def __init__(self, message: str):
        """Event not found"""
        super().__init__(message)


class EventNotCreatedError(Exception):
    def __init__(self, message: str):
        """Event could not be created"""
        super().__init__(message)


class EventSoldOutError(Exception):
    def __init__(self, message: str):
        """Event has sold out and cannot proceed with the registration"""
        super().__init__(message)
