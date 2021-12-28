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
    current_user_pk: Optional[TPrimaryKey] = None,
) -> List[Company]:
    async with uow:
        company_pks = [o.company_pk for o in await uow.companies_m2m_contractors.filter(contractor_pk=current_user_pk)]
        companies = await uow.companies.list(
            search=message.search,
            sort_by=message.sort_by,
            limit=message.limit,
            offset=message.offset,
            pk__in=company_pks,
        )
    return companies


@has_role(role=TRole.CONTRACTOR)
async def company_retrieve_handler(
    message: ContractorCompanyRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> Company:
    async with uow:
        if not await uow.companies_m2m_contractors.exists(contractor_pk=current_user_pk, company_pk=message.company_pk):
            raise PermissionDeniedException(detail=f"Contractor has no access to company with pk {message.company_pk}")
        company = await uow.companies.get(pk=message.pk)
    return company


@has_role(role=TRole.CONTRACTOR)
async def company_leave_handler(
    message: ContractorCompanyLeaveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> None:
    async with uow:
        company_m2m_contractor = await uow.companies_m2m_contractors.first(
            contractor_pk=current_user_pk,
            company_pk=message.company_pk,
        )
        if not company_m2m_contractor:
            raise PermissionDeniedException(detail=f"Contractor has no access to company with pk {message.company_pk}")
        uow.companies_m2m_contractors.delete(company_m2m_contractor.pk)
