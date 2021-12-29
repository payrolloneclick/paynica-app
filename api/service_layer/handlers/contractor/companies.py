from typing import List, Optional

from domain.commands.contractor.companies import (
    ContractorCompanyLeaveCommand,
    ContractorCompanyListCommand,
    ContractorCompanyRetrieveCommand,
)
from domain.models.companies import Company
from domain.types import TPrimaryKey, TRole
from service_layer.exceptions import PermissionDeniedException
from service_layer.unit_of_work.db import DBUnitOfWork

from ..permissions import has_role


@has_role(role=TRole.CONTRACTOR)
async def company_list_handler(
    message: ContractorCompanyListCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> List[Company]:
    async with uow:
        company_ids = [o.company_id for o in await uow.companies_m2m_contractors.filter(contractor_id=current_user_id)]
        companies = await uow.companies.list(
            search=message.search,
            sort_by=message.sort_by,
            limit=message.limit,
            offset=message.offset,
            id__in=company_ids,
        )
    return companies


@has_role(role=TRole.CONTRACTOR)
async def company_retrieve_handler(
    message: ContractorCompanyRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> Company:
    async with uow:
        if not await uow.companies_m2m_contractors.exists(contractor_id=current_user_id, company_id=message.company_id):
            raise PermissionDeniedException(detail=f"Contractor has no access to company with id {message.company_id}")
        company = await uow.companies.get(id=message.company_id)
    return company


@has_role(role=TRole.CONTRACTOR)
async def company_leave_handler(
    message: ContractorCompanyLeaveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> None:
    async with uow:
        company_m2m_contractor = await uow.companies_m2m_contractors.first(
            contractor_id=current_user_id,
            company_id=message.company_id,
        )
        if not company_m2m_contractor:
            raise PermissionDeniedException(detail=f"Contractor has no access to company with id {message.company_id}")
        await uow.companies_m2m_contractors.delete(company_m2m_contractor.id)
        await uow.commit()
