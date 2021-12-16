from typing import List

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.employer.bank_accounts import (
    EmployerSenderBankAccountCreateCommand,
    EmployerSenderBankAccountDeleteCommand,
    EmployerSenderBankAccountListCommand,
    EmployerSenderBankAccountRetrieveCommand,
    EmployerSenderBankAccountUpdateCommand,
)
from domain.responses.bank_accounts import SenderBankAccountResponse
from domain.types import TPrimaryKey

from ..dependencies import get_current_employer_pk

router = APIRouter(
    prefix="/employer/sender-bank-accounts",
    tags=["employer-sender-bank-accounts"],
)


@router.get("/", response_model=List[SenderBankAccountResponse])
async def get_sender_bank_accounts(
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get sender bank accounts list for authenticated employer."""
    result = await bus.handler(EmployerSenderBankAccountListCommand(), current_user_pk=current_employer_pk)
    return [SenderBankAccountResponse(**o.dict()) for o in result]


@router.get("/{sender_bank_account_pk}", response_model=SenderBankAccountResponse)
async def get_sender_bank_account(
    sender_bank_account_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get a sender bank account for authenticated employer."""
    command = EmployerSenderBankAccountRetrieveCommand(sender_bank_account_pk=sender_bank_account_pk)
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return SenderBankAccountResponse(**result.dict())


@router.post("/", response_model=SenderBankAccountResponse)
async def create_sender_bank_account(
    command: EmployerSenderBankAccountCreateCommand,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Create a sender bank account for authenticated employer."""
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return SenderBankAccountResponse(**result.dict())


@router.patch("/{sender_bank_account_pk}", response_model=SenderBankAccountResponse)
async def update_sender_bank_account(
    sender_bank_account_pk: TPrimaryKey,
    command: EmployerSenderBankAccountUpdateCommand,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Update a sender bank account for authenticated employer."""
    command.sender_bank_account_pk = sender_bank_account_pk
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return SenderBankAccountResponse(**result.dict())


@router.delete("/{sender_bank_account_pk}")
async def delete_sender_bank_account(
    sender_bank_account_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Delete/inactivate a sender bank account for authenticated employer."""
    command = EmployerSenderBankAccountDeleteCommand(sender_bank_account_pk=sender_bank_account_pk)
    await bus.handler(command, current_user_pk=current_employer_pk)
