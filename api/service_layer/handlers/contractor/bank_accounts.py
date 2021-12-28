from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from domain.commands.contractor.bank_accounts import (
    ContractorRecipientBankAccountCreateCommand,
    ContractorRecipientBankAccountDeleteCommand,
    ContractorRecipientBankAccountListCommand,
    ContractorRecipientBankAccountRetrieveCommand,
    ContractorRecipientBankAccountUpdateCommand,
)
from domain.models.bank_accounts import RecipientBankAccount
from domain.types import TPrimaryKey, TRole
from service_layer.exceptions import PermissionDeniedException
from service_layer.unit_of_work.db import DBUnitOfWork

from ..permissions import has_role


@has_role(role=TRole.CONTRACTOR)
async def recipient_bank_account_list_handler(
    message: ContractorRecipientBankAccountListCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> List[RecipientBankAccount]:
    async with uow:
        recipient_bank_accounts = await uow.recipient_bank_accounts.list(
            search=message.search,
            sort_by=message.sort_by,
            limit=message.limit,
            offset=message.offset,
            recipient_owner_user_pk=current_user_pk,
            recipient_owner_company_pk=current_company_pk,
        )
    return recipient_bank_accounts


@has_role(role=TRole.CONTRACTOR)
async def recipient_bank_account_retrieve_handler(
    message: ContractorRecipientBankAccountRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> RecipientBankAccount:
    async with uow:
        recipient_bank_account = await uow.recipient_bank_accounts.get(
            pk=message.recipient_bank_account_pk,
            recipient_owner_user_pk=current_user_pk,
            recipient_owner_company_pk=current_company_pk,
        )
    return recipient_bank_account


@has_role(role=TRole.CONTRACTOR)
async def recipient_bank_account_create_handler(
    message: ContractorRecipientBankAccountCreateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> RecipientBankAccount:
    async with uow:
        recipient_bank_account = RecipientBankAccount(
            pk=uuid4(),
            created_date=datetime.utcnow(),
            recipient_owner_user_pk=current_user_pk,
            recipient_owner_company_pk=current_company_pk,
            recipient_currency=message.recipient_currency,
            recipient_country_alpha3=message.recipient_country_alpha3,
        )
        await uow.recipient_bank_accounts.add(recipient_bank_account)
        await uow.commit()
    return recipient_bank_account


@has_role(role=TRole.CONTRACTOR)
async def recipient_bank_account_update_handler(
    message: ContractorRecipientBankAccountUpdateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> RecipientBankAccount:
    async with uow:
        recipient_bank_account = await uow.recipient_bank_accounts.get(
            pk=message.recipient_bank_account_pk,
            recipient_owner_user_pk=current_user_pk,
            recipient_owner_company_pk=current_company_pk,
        )
        if message.recipient_currency is not None:
            recipient_bank_account.recipient_currency = message.recipient_currency
        if message.recipient_country_alpha3 is not None:
            recipient_bank_account.recipient_country_alpha3 = message.recipient_country_alpha3
        recipient_bank_account.updated_date = datetime.utcnow()
        await uow.recipient_bank_accounts.update(recipient_bank_account)
        await uow.commit()
    return recipient_bank_account


@has_role(role=TRole.CONTRACTOR)
async def recipient_bank_account_delete_handler(
    message: ContractorRecipientBankAccountDeleteCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> None:
    async with uow:
        if not await uow.recipient_bank_accounts.exists(
            pk=message.recipient_bank_account_pk,
            recipient_owner_user_pk=current_user_pk,
            recipient_owner_company_pk=current_company_pk,
        ):
            raise PermissionDeniedException(detail="User has no access to delete this recipient bank account")
        await uow.recipient_bank_accounts.delete(message.recipient_bank_account_pk)
        await uow.commit()
