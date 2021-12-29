from functools import wraps
from typing import Optional

from domain.types import TRole
from service_layer.exceptions import PermissionDeniedException, ServiceException


def has_role(function=None, role: Optional[TRole] = TRole.EMPLOYER):
    def decorator(fn):
        @wraps(fn)
        async def wrap(*args, **kwargs):
            uow = kwargs.get("uow")
            current_user_id = kwargs.get("current_user_id")
            if not uow:
                raise ServiceException(detail="No uow in arguments")
            if not current_user_id:
                raise ServiceException(detail="No current_user_id in arguments")
            if not await uow.users.exists(id=current_user_id, role=role):
                raise PermissionDeniedException(detail=f"User dosn't have role {role}")
            return await fn(*args, **kwargs)

        return wrap

    if function:
        return decorator(function)
    return decorator
