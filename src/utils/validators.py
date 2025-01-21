"""
### Validators
This module contains useful validations to be used in this project.

Functions:

    email_validator(email:str)->bool
    name_validator(name:str)->bool
"""

import re


def email_validator(email: str) -> bool:
    """
    This function is a helper to validate format of a given email.
    Parameters:
        email (str): The email to be checked
    Returns: is_valid (bool) : The result of the validation
    """
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if isinstance(email, str) and re.fullmatch(regex, email):
        return True
    return False


def name_validator(name: str) -> bool:
    """
    This function is a helper to validate the format of a given name.
    Parameters:
        name (str): The name to be checked
    Returns: is_valid (bool) : The result of the validation
    """
    regex = r"^[A-Za-z\s]{4,}$"
    if (
        isinstance(name, str)
        and re.fullmatch(regex, name)
        and not any(char.isdigit() for char in name)
    ):
        return True
    return False
