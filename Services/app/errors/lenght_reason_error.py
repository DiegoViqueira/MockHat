

class LenghtReasonError(Exception):
    """Exception raised when the length of the reason is too long."""

    def __init__(self, message: str = "The length of the reason is too long."):
        self.message = message
        super().__init__(self.message)
