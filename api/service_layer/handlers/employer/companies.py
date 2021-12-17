from datetime import datetime
from typing import Optional
from uuid import uuid4

from domain.commands.employer.companies import EmployerCompanyCreateCommand
from domain.models.companies import Company, CompanyM2MEmployer
from domain.types import TPrimaryKey, TRole
from service_layer.exceptions import PermissionDeniedException
from service_layer.unit_of_work.db import DBUnitOfWork


async def company_create_handler(
    message: EmployerCompanyCreateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> Company:
    company = Company(
        pk=uuid4(),
        name=message.name,
        owner_pk=current_user_pk,
        created_date=datetime.now(),
    )
    company_m2m_employer = CompanyM2MEmployer(
        pk=uuid4(),
        company_pk=company.pk,
        employer_pk=current_user_pk,
        created_date=datetime.now(),
    )
    async with uow:
        if await uow.users.exists(pk=current_user_pk, role=TRole.CONTRACTOR):
            raise PermissionDeniedException(detail="Contractor cannot create a company")
        await uow.companies.add(company)
        await uow.companies_m2m_employers.add(company_m2m_employer)
        await uow.commit()
    return company
