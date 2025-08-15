class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message=None) -> None:
        if message is not None:
            self.message = message


class NotFoundException(BaseException):
    message = "Not Found"


class InsertException(BaseException):
    message = "Error inserting document"

