from typing import List, Optional

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
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_user_pk

router = APIRouter(
    prefix="/contractor/recipient-bank-accounts",
    tags=["contractor-recipient-bank-accounts"],
)


@router.get("/", response_model=List[RecipientBankAccountResponse])
async def get_recipient_bank_accounts(
    company_pk: Optional[TPrimaryKey] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Get recipient bank accounts list for authenticated contractor."""
    command = ContractorRecipientBankAccountListCommand()
    command.recipient_owner_company_pk = company_pk
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return [RecipientBankAccountResponse(**o.dict()) for o in result]


@router.get("/{recipient_bank_account_pk}", response_model=RecipientBankAccountResponse)
async def get_recipient_bank_account(
    recipient_bank_account_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Get a recipient bank account for authenticated contractor."""
    command = ContractorRecipientBankAccountRetrieveCommand(recipient_bank_account_pk=recipient_bank_account_pk)
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return RecipientBankAccountResponse(**result.dict())


@router.post("/", response_model=RecipientBankAccountResponse)
async def create_recipient_bank_account(
    command: ContractorRecipientBankAccountCreateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Create a recipient bank account for authenticated contractor."""
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return RecipientBankAccountResponse(**result.dict())


@router.patch("/{recipient_bank_account_pk}", response_model=RecipientBankAccountResponse)
async def update_recipient_bank_account(
    recipient_bank_account_pk: TPrimaryKey,
    command: ContractorRecipientBankAccountUpdateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Update a recipient bank account for authenticated contractor."""
    command.recipient_bank_account_pk = recipient_bank_account_pk
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return RecipientBankAccountResponse(**result.dict())


@router.delete("/{recipient_bank_account_pk}")
async def delete_recipient_bank_account(
    recipient_bank_account_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Delete/inactivate a recipient bank account for authenticated contractor."""
    command = ContractorRecipientBankAccountDeleteCommand(recipient_bank_account_pk=recipient_bank_account_pk)
    await bus.handler(command, current_user_pk=current_contractor_pk)
