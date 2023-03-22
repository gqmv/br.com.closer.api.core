class NullTaxIdError(Exception):
    """
    Raised when an attempt is made to create a user with a null tax id
    """

    def __init__(self, message: str = "Users must have a tax_id."):
        self.message = message
        super().__init__(message)


class InvalidPermissionError(Exception):
    """
    Raised when an attempt is made to create a user with an invalid permission (i.e. is_staff is not True when a superuser is created).
    """

    def __init__(self, message: str = "Invalid permission."):
        self.message = message
        super().__init__(message)
