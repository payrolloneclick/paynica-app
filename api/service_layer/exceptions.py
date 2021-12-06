from typing import Any


class ServiceException(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__()
        self.detail = detail


class PermissionDeniedException(ServiceException):
    pass


class ValidationException(ServiceException):
    pass
