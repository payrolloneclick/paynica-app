from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic.types import UUID4

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
from domain.models.operations import Account, Operation
from service_layer.unit_of_work.db import DBUnitOfWork

from ..exceptions import PermissionDeniedException


async def create_account_handler(
    message: CreateAccountCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> Account:
    async with uow:
        user = uow.users.get(pk=current_user_pk)
        account = Account(
            pk=uuid4(),
            user=user,
            currency=message.currency,
            country_alpha3=message.country_alpha3,
            created_date=datetime.now(),
        )
        await uow.accounts.add(account)
        await uow.commit()
    return account


async def update_account_handler(
    message: UpdateAccountCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> Account:
    async with uow:
        account = await uow.accounts.get(pk=message.pk)
        if account.user.pk != current_user_pk:
            raise PermissionDeniedException(detail="User doesn't have permissions to update the account")
        if message.currency:
            account.currency = message.currency
        if message.country_alpha3:
            account.country_alpha3 = message.country_alpha3
        account.updated_date = datetime.now()
        await uow.accounts.update(account)
        await uow.commit()
    return account


async def retrieve_accounts_handler(
    message: RetrieveAccountsCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> List[Account]:
    async with uow:
        # TODO
        accounts = await uow.accounts.all()
    return accounts


async def retrieve_account_handler(
    message: RetrieveAccountCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> List[Account]:
    async with uow:
        account = await uow.accounts.get(pk=message.pk)
    return account


async def retrieve_recipient_accounts_handler(
    message: RetrieveRecipientAccountsCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> List[Account]:
    async with uow:
        # TODO
        accounts = await uow.accounts.all()
    return accounts


async def delete_account_handler(
    message: DeleteAccountCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> DeleteAccountCommand:
    async with uow:
        if message.pk != current_user_pk:
            raise PermissionDeniedException("User doesn't have permissions to delete the account")
        await uow.accounts.delete(message.pk)
        await uow.commit()
    return message


async def create_operation_handler(
    message: CreateOperationCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> Operation:
    async with uow:
        user = uow.users.get(pk=current_user_pk)
        # TODO
        operation = Operation(
            pk=uuid4(),
            user=user,
            created_date=datetime.now(),
        )
        await uow.operations.add(operation)
        await uow.commit()
    return operation


async def update_operation_handler(
    message: UpdateOperationCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> Operation:
    async with uow:
        operation = await uow.operations.get(pk=message.pk)
        if operation.user.pk != current_user_pk:
            raise PermissionDeniedException(detail="User doesn't have permissions to update the operation")
        # TODO
        operation.updated_date = datetime.now()
        await uow.operations.update(operation)
        await uow.commit()
    return operation


async def retrieve_operations_handler(
    message: RetrieveOperationsCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> List[Operation]:
    async with uow:
        # TODO
        operations = await uow.operations.all()
    return operations


async def retrieve_operation_handler(
    message: RetrieveOperationCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> List[Operation]:
    async with uow:
        operation = await uow.operations.get(pk=message.pk)
        if operation.user.pk != current_user_pk:
            raise PermissionDeniedException(detail="User doesn't have permissions to retrieve the operation")
    return operation
