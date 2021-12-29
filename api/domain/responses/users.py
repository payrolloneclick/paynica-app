from datetime import datetime
from typing import Optional

from ..types import TEmail, TPhone, TPrimaryKey
from .generic import AbstractReponse


class UserResponse(AbstractReponse):
    id: Optional[TPrimaryKey]
    email: Optional[TEmail]
    phone: Optional[TPhone]
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
