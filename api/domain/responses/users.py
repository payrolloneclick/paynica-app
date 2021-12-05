from datetime import datetime
from typing import Optional

from pydantic.types import UUID4

from .generic import AbstractReponse


class UserResponse(AbstractReponse):
    pk: Optional[UUID4]
    email: Optional[str]
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class GenerateAccessTokenResponse(AbstractReponse):
    access_token: str
    access_token_expired_at: datetime
    refresh_token: str
    refresh_token_expired_at: datetime


class RefreshAccessTokenResponse(AbstractReponse):
    access_token: str
    access_token_expired_at: datetime
