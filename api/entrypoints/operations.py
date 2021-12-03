# from typing import List

from typing import List

from fastapi import APIRouter, Depends
from pydantic.types import UUID4

from bootstrap import bus
from domain.commands.operations import (
    CreateAccountCommand,
    CreateOperationCommand,
    DeleteAccountCommand,
    RetrieveAccountCommand,
    RetrieveAccountsCommand,
    RetrieveOperationCommand,
    RetrieveOperationsCommand,
    RetrieveRecipientAccountsCommand,
    UpdateAccountCommand,
    UpdateOperationCommand,
)
from domain.responses.operations import AccountResponse, OperationResponse

from .dependencies import get_current_user_pk

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
)


@router.get("/accounts", response_model=List[AccountResponse])
async def get_accounts(
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Get accounts for authenticated user."""
    result = await bus.handler(RetrieveAccountsCommand(), current_user_pk=current_user_pk)
    return [AccountResponse(**o.dict()) for o in result]


@router.post("/accounts", response_model=AccountResponse)
async def create_account(
    command: CreateAccountCommand,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Create an account for authenticated user."""
    result = await bus.handler(command, current_user_pk=current_user_pk)
    return AccountResponse(**result.dict())


@router.get("/accounts/{pk}", response_model=AccountResponse)
async def get_account(
    pk: UUID4,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Get an account for authenticated user."""
    result = await bus.handler(RetrieveAccountCommand(pk=pk), current_user_pk=current_user_pk)
    return AccountResponse(**result.dict())


@router.patch("/accounts/{pk}", response_model=AccountResponse)
async def update_account(
    pk: UUID4,
    command: UpdateAccountCommand,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Update an account for authenticated user."""
    command.pk = pk
    result = await bus.handler(command, current_user_pk=current_user_pk)
    return AccountResponse(**result.dict())


@router.delete("/accounts/{pk}")
async def delete_account(
    pk: UUID4,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Delete/inactivate account of authenticated user."""
    result = await bus.handler(DeleteAccountCommand(pk=pk), current_user_pk=current_user_pk)
    return AccountResponse(**result.dict())


@router.get("/recipient-accounts", response_model=List[AccountResponse])
async def get_recipient_accounts(
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Get recipients accounts to create an operation."""
    result = await bus.handler(RetrieveRecipientAccountsCommand(), current_user_pk=current_user_pk)
    return [AccountResponse(**o.dict()) for o in result]


@router.get("/operations", response_model=List[OperationResponse])
async def get_operations(
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Get operations for authenticated user."""
    result = await bus.handler(RetrieveOperationsCommand(), current_user_pk=current_user_pk)
    return [OperationResponse(**o.dict()) for o in result]


@router.post("/operations", response_model=OperationResponse)
async def create_operation(
    command: CreateOperationCommand,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Create an operation for authenticated user."""
    result = await bus.handler(command, current_user_pk=current_user_pk)
    return OperationResponse(**result.dict())


@router.patch("/operations/{pk}", response_model=OperationResponse)
async def update_operation(
    pk: UUID4,
    command: UpdateOperationCommand,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Create an operation for authenticated user."""
    command.pk = pk
    result = await bus.handler(command, current_user_pk=current_user_pk)
    return OperationResponse(**result.dict())


@router.get("/operations/{pk}", response_model=OperationResponse)
async def get_operation(pk: UUID4, current_user_pk: UUID4 = Depends(get_current_user_pk)):
    """Get an operation for authenticated user."""
    result = await bus.handler(RetrieveOperationCommand(pk=pk), current_user_pk=current_user_pk)
    return OperationResponse(**result.dict())
