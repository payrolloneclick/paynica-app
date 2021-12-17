from typing import Optional

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.types import TPrimaryKey
from service_layer.exceptions import ValidationException
from settings import DEFAULT_LIMIT

from .dependencies import get_current_admin_pk

router = APIRouter(
    tags=["admin"],
)


@router.get("/resources/{resource_key}")
async def list(
    resource_key: str,
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_user_pk: TPrimaryKey = Depends(get_current_admin_pk),
):
    async with bus.uow:
        if resource_key not in bus.admin_resources.resources:
            raise ValidationException(detail=f"Invalid resource key {resource_key}")
        resource = bus.admin_resources.resources[resource_key]
        return await resource.list(
            offset=offset,
            limit=limit,
            search=search,
            sort_by=sort_by,
        )


@router.get("/resources/{resource_key}/{pk}")
async def get(
    resource_key: str,
    pk: TPrimaryKey,
    current_user_pk: str = Depends(get_current_admin_pk),
):
    async with bus.uow:
        if resource_key not in bus.admin_resources.resources:
            raise ValidationException(detail=f"Invalid resource key {resource_key}")
        resource = bus.admin_resources.resources[resource_key]
        return await resource.retrieve(pk)


@router.post("/resources/{resource_key}")
async def create(
    resource_key: str,
    payload: dict,
    current_user_pk: str = Depends(get_current_admin_pk),
):
    async with bus.uow:
        if resource_key not in bus.admin_resources.resources:
            raise ValidationException(detail=f"Invalid resource key {resource_key}")
        resource = bus.admin_resources.resources[resource_key]
        return await resource.create(payload)


@router.patch("/resources/{resource_key}/{pk}")
async def update(
    resource_key: str,
    pk: TPrimaryKey,
    payload: dict,
    current_user_pk: str = Depends(get_current_admin_pk),
):
    async with bus.uow:
        if resource_key not in bus.admin_resources.resources:
            raise ValidationException(detail=f"Invalid resource key {resource_key}")
        resource = bus.admin_resources.resources[resource_key]
        return await resource.update(pk, payload)


@router.delete("/resources/{resource_key}/{pk}")
async def delete(
    resource_key: str,
    pk: TPrimaryKey,
    current_user_pk: str = Depends(get_current_admin_pk),
):
    async with bus.uow:
        if resource_key not in bus.admin_resources.resources:
            raise ValidationException(detail=f"Invalid resource key {resource_key}")
        resource = bus.admin_resources.resources[resource_key]
        return await resource.delete(pk)
