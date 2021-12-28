from typing import Any


class EntrypointsException(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__()
        self.detail = detail


class NotAuthorizedException(EntrypointsException):
    pass


class HeaderValidationException(EntrypointsException):
    pass
