from typing import Any


class NotAuthorizedException(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__()
        self.detail = detail
