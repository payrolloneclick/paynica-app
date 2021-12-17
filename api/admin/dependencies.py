from fastapi import Depends
from fastapi.security import HTTPBearer

from bootstrap import bus
from entrypoints.dependencies import get_current_user_pk
from service_layer.exceptions import PermissionDeniedException

token_auth_scheme = HTTPBearer()


async def get_current_admin_pk(token: str = Depends(token_auth_scheme)):
    current_user_pk = await get_current_user_pk(token)
    async with bus.uow:
        if not await bus.uow.users.exists(pk=current_user_pk, is_superuser=True):
            raise PermissionDeniedException(detail="User has no access to this endpoint")
    return current_user_pk


# disable auth
# async def get_current_admin_pk():
#     pass
