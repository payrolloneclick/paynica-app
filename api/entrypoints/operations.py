# from typing import List

from typing import List
from fastapi import APIRouter, Depends

from pydantic.types import UUID4

from service_layer.services import operations as operations_services
from bootstrap import uow

from .dependencies import get_current_user_pk
from .schemas.operations import (
    AccountCreateRequest,
    AccountResponse,
    AccountUpdateRequest,
    OperationCreateRequest,
    OperationResponse,
)

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
)


@router.get("/accounts", response_model=List[AccountResponse])
async def get_accounts(current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Get accounts for authenticated user."""
    accounts = await operations_services.get_accounts_for_user(uow, current_user_pk)
    return [AccountResponse(**o.dict()) for o in accounts]


@router.post("/accounts", response_model=AccountResponse)
async def create_account(body: AccountCreateRequest, current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Create an account for authenticated user."""
    account = await operations_services.create_account_for_user(
        uow,
        current_user_pk,
        **body.dict(exclude_unset=True, exclude_none=True),
    )
    return AccountResponse(**account.dict())


@router.get("/accounts/{pk}", response_model=AccountResponse)
async def get_account(pk: UUID4, current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Get an account for authenticated user."""
    account = await operations_services.get_account_for_user(uow, current_user_pk, pk)
    return AccountResponse(**account.dict())


@router.patch("/accounts/{pk}", response_model=AccountResponse)
async def update_account(
    pk: UUID4,
    body: AccountUpdateRequest,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Update an account for authenticated user."""
    account = await operations_services.update_account_for_user(
        uow,
        current_user_pk,
        pk,
        **body.dict(exclude_unset=True, exclude_none=True),
    )
    return AccountResponse(**account.dict())


@router.delete("/accounts/{pk}")
async def delete_account(pk: UUID4, current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Delete/inactivate account of authenticated user."""
    pk = await operations_services.delete_account_for_user(uow, current_user_pk, pk)
    return pk


@router.get("/recipient-accounts", response_model=List[AccountResponse])
async def get_recipient_accounts(current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Get recipients accounts to create an operation."""
    recipient_accounts = await operations_services.get_recipient_accounts_for_user(uow, current_user_pk)
    return [AccountResponse(**o.dict()) for o in recipient_accounts]


@router.get("/operations", response_model=List[OperationResponse])
async def get_operations(current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Get operations for authenticated user."""
    operations = await operations_services.get_operations_for_user(uow, current_user_pk)
    return [OperationResponse(**o.dict()) for o in operations]


@router.post("/operations", response_model=OperationResponse)
async def create_operation(body: OperationCreateRequest, current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Create an operation for authenticated user."""
    operation = await operations_services.create_operation_for_user(
        uow,
        current_user_pk,
        **body.dict(exclude_unset=True, exclude_none=True),
    )
    return OperationResponse(**operation.dict())


@router.patch("/operations/{pk}", response_model=OperationResponse)
async def update_operation(pk: UUID4, body: OperationCreateRequest, current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Create an operation for authenticated user."""
    operation = await operations_services.update_operation_for_user(
        uow,
        current_user_pk,
        pk,
        **body.dict(exclude_unset=True, exclude_none=True),
    )
    return OperationResponse(**operation.dict())


@router.get("/operations/{pk}", response_model=OperationResponse)
async def get_operation(pk: UUID4, current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Get an operation for authenticated user."""
    operation = await operations_services.get_operation_for_user(uow, current_user_pk, pk)
    return OperationResponse(**operation.dict())
