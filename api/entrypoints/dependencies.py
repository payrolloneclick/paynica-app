from datetime import datetime
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer

from entrypoints.exceptions import NotAuthorizedException
from settings import JWT_SECRET_KEY

token_auth_scheme = HTTPBearer()


async def get_current_user_pk(token: str = Depends(token_auth_scheme)):
    try:
        decoded_access_token = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise NotAuthorizedException("Invalid access token")
    access_token_expired_at = decoded_access_token.get("access_token_expired_at")
    user_pk = decoded_access_token.get("user_pk")
    if not access_token_expired_at or not user_pk:
        raise NotAuthorizedException("Invalid payload for access token")
    expired_at = datetime.fromisoformat(access_token_expired_at)
    now = datetime.utcnow()
    if expired_at < now:
        raise NotAuthorizedException("Expired access token")
    return UUID(user_pk)


async def get_current_employer_pk(token: str = Depends(token_auth_scheme)):
    user_pk = get_current_user_pk(token)
    # TODO check role employer
    return user_pk


async def get_current_contractor_pk(token: str = Depends(token_auth_scheme)):
    user_pk = get_current_user_pk(token)
    # TODO check role contractor
    return user_pk
