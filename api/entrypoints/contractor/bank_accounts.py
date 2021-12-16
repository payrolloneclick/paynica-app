from typing import List

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.contractor.bank_accounts import (
    ContractorRecipientBankAccountCreateCommand,
    ContractorRecipientBankAccountDeleteCommand,
    ContractorRecipientBankAccountListCommand,
    ContractorRecipientBankAccountRetrieveCommand,
    ContractorRecipientBankAccountUpdateCommand,
)
from domain.responses.bank_accounts import RecipientBankAccountResponse
from domain.types import TPrimaryKey

from ..dependencies import get_current_contractor_pk

router = APIRouter(
    prefix="/contractor/recipient-bank-accounts",
    tags=["contractor-recipient-bank-accounts"],
)


@router.get("/", response_model=List[RecipientBankAccountResponse])
async def get_recipient_bank_accounts(
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Get recipient bank accounts list for authenticated contractor."""
    result = await bus.handler(ContractorRecipientBankAccountListCommand(), current_user_pk=current_contractor_pk)
    return [RecipientBankAccountResponse(**o.dict()) for o in result]


@router.get("/{recipient_bank_account_pk}", response_model=RecipientBankAccountResponse)
async def get_recipient_bank_account(
    recipient_bank_account_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Get a recipient bank account for authenticated contractor."""
    command = ContractorRecipientBankAccountRetrieveCommand(recipient_bank_account_pk=recipient_bank_account_pk)
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return RecipientBankAccountResponse(**result.dict())


@router.post("/", response_model=RecipientBankAccountResponse)
async def create_recipient_bank_account(
    command: ContractorRecipientBankAccountCreateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Create a recipient bank account for authenticated contractor."""
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return RecipientBankAccountResponse(**result.dict())


@router.patch("/{recipient_bank_account_pk}", response_model=RecipientBankAccountResponse)
async def update_recipient_bank_account(
    recipient_bank_account_pk: TPrimaryKey,
    command: ContractorRecipientBankAccountUpdateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Update a recipient bank account for authenticated contractor."""
    command.recipient_bank_account_pk = recipient_bank_account_pk
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return RecipientBankAccountResponse(**result.dict())


@router.delete("/{recipient_bank_account_pk}")
async def delete_recipient_bank_account(
    recipient_bank_account_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Delete/inactivate a recipient bank account for authenticated contractor."""
    command = ContractorRecipientBankAccountDeleteCommand(recipient_bank_account_pk=recipient_bank_account_pk)
    await bus.handler(command, current_user_pk=current_contractor_pk)
