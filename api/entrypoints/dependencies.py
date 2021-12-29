from datetime import datetime
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request

from bootstrap import bus
from entrypoints.exceptions import HeaderValidationException, NotAuthorizedException
from settings import JWT_SECRET_KEY

token_auth_scheme = HTTPBearer()


async def get_current_user_id(token: str = Depends(token_auth_scheme)) -> UUID:
    try:
        decoded_access_token = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise NotAuthorizedException("Invalid access token")
    access_token_expired_at = decoded_access_token.get("access_token_expired_at")
    user_id = decoded_access_token.get("user_id")
    if not access_token_expired_at or not user_id:
        raise NotAuthorizedException("Invalid payload for access token")
    expired_at = datetime.fromisoformat(access_token_expired_at)
    now = datetime.utcnow()
    if expired_at < now:
        raise NotAuthorizedException("Expired access token")

    async with bus.uow:
        if not await bus.uow.users.exists(id=UUID(user_id), is_active=True):
            raise NotAuthorizedException(detail="Please finish signup process for this user")
    return UUID(user_id)


async def get_current_company_id(request: Request) -> UUID:
    company_id: str = request.headers.get("Company")
    if not company_id:
        raise HeaderValidationException(detail="No company id in headers of request")
    return UUID(company_id)
