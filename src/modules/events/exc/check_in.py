class AlreadyCheckedInError(Exception):
    def __init__(self, message: str):
        """Check in has already made before"""
        super().__init__(message)


class CheckInNotRegistered(Exception):
    def __init__(self, message: str):
        """Check in could not be registered"""
        super().__init__(message)
