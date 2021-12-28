from typing import List, Optional

from domain.commands.contractor.operations import ContractorOperationListCommand, ContractorOperationRetrieveCommand
from domain.models.operations import Operation
from domain.types import TPrimaryKey, TRole
from service_layer.unit_of_work.db import DBUnitOfWork

from ..permissions import has_role


@has_role(role=TRole.CONTRACTOR)
async def operation_list_handler(
    message: ContractorOperationListCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> List[Operation]:
    async with uow:
        operations = await uow.operations.list(
            search=message.search,
            sort_by=message.sort_by,
            limit=message.limit,
            offset=message.offset,
            operation_recipient_user_pk=current_user_pk,
            operation_owner_company_pk=current_company_pk,
        )
    return operations


@has_role(role=TRole.CONTRACTOR)
async def operation_retrieve_handler(
    message: ContractorOperationRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> Operation:
    async with uow:
        operation = await uow.operations.get(
            pk=message.recipient_bank_account_pk,
            operation_recipient_user_pk=current_user_pk,
            operation_owner_company_pk=current_company_pk,
        )
        operation.sender_account = await uow.sender_bank_accounts.get(pk=operation.sender_account_pk)
        operation.recipient_account = await uow.recipient_bank_accounts.get(pk=operation.recipient_account_pk)
    return operation
