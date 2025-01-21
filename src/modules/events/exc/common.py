class ValidationError(Exception):
    def __init__(self, message: str):
        """The field provided is not valid"""
        super().__init__(message)
