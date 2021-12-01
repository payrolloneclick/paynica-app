from typing import Any


class RepositoryException(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__()
        self.detail = detail


class ObjectAlreadyExists(RepositoryException):
    pass


class ObjectDoesNotExist(RepositoryException):
    pass


class MultipleObjectsReturned(RepositoryException):
    pass
