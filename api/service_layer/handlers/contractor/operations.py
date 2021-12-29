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
    current_user_id: Optional[TPrimaryKey] = None,
    current_company_id: Optional[TPrimaryKey] = None,
) -> List[Operation]:
    async with uow:
        operations = await uow.operations.list(
            search=message.search,
            sort_by=message.sort_by,
            limit=message.limit,
            offset=message.offset,
            operation_recipient_user_id=current_user_id,
            operation_owner_company_id=current_company_id,
        )
    return operations


@has_role(role=TRole.CONTRACTOR)
async def operation_retrieve_handler(
    message: ContractorOperationRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
    current_company_id: Optional[TPrimaryKey] = None,
) -> Operation:
    async with uow:
        operation = await uow.operations.get(
            id=message.recipient_bank_account_id,
            operation_recipient_user_id=current_user_id,
            operation_owner_company_id=current_company_id,
        )
        operation.sender_account = await uow.sender_bank_accounts.get(id=operation.sender_account_id)
        operation.recipient_account = await uow.recipient_bank_accounts.get(id=operation.recipient_account_id)
    return operation
