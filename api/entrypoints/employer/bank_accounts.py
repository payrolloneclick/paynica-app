from typing import List, Optional

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
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_company_id, get_current_user_id

router = APIRouter(
    prefix="/employer/sender-bank-accounts",
    tags=["employer-sender-bank-accounts"],
)


@router.get("", response_model=List[SenderBankAccountResponse])
async def get_sender_bank_accounts(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get sender bank accounts list for authenticated employer."""
    command = EmployerSenderBankAccountListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return [SenderBankAccountResponse(**o.dict()) for o in result]


@router.get("/{sender_bank_account_id}", response_model=SenderBankAccountResponse)
async def get_sender_bank_account(
    sender_bank_account_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get a sender bank account for authenticated employer."""
    command = EmployerSenderBankAccountRetrieveCommand(sender_bank_account_id=sender_bank_account_id)
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return SenderBankAccountResponse(**result.dict())


@router.post("", response_model=SenderBankAccountResponse)
async def create_sender_bank_account(
    command: EmployerSenderBankAccountCreateCommand,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Create a sender bank account for authenticated employer."""
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return SenderBankAccountResponse(**result.dict())


@router.patch("/{sender_bank_account_id}", response_model=SenderBankAccountResponse)
async def update_sender_bank_account(
    sender_bank_account_id: TPrimaryKey,
    command: EmployerSenderBankAccountUpdateCommand,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Update a sender bank account for authenticated employer."""
    command.sender_bank_account_id = sender_bank_account_id
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return SenderBankAccountResponse(**result.dict())


@router.delete("/{sender_bank_account_id}")
async def delete_sender_bank_account(
    sender_bank_account_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Delete/inactivate a sender bank account for authenticated employer."""
    command = EmployerSenderBankAccountDeleteCommand(sender_bank_account_id=sender_bank_account_id)
    await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
