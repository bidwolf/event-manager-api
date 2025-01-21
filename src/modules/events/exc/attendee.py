class AttendeeNotCreatedError(Exception):
    def __init__(self, message: str):
        """Attendee could not be created in the database"""
        super().__init__(message)


class AttendeeAlreadyExistsError(Exception):
    def __init__(self, message: str):
        """Attendee already registered on this Event"""
        super().__init__(message)


class AttendeeNotFoundError(Exception):
    def __init__(self, message: str):
        """Attendee not found"""
        super().__init__(message)
