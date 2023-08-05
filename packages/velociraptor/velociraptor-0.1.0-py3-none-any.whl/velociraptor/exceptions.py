"""
Manually defined exceptions.
"""


class RegistrationDoesNotMatchError(Exception):
    """
    Raised when our registration function does not match the current
    variable name passed to it.
    """

    def __init__(self, message=""):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

