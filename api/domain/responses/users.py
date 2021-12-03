from typing import Optional

from pydantic.types import UUID4

from .generic import AbstractReponse


class UserResponse(AbstractReponse):
    pk: Optional[UUID4]
    email: Optional[str]
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
