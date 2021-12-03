from fastapi import Depends
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()


async def get_current_user_pk(token: str = Depends(token_auth_scheme)):
    # TODO: get pk from jwt token
    return token.credentials
