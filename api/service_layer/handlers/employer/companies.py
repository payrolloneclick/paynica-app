from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from domain.commands.employer.companies import (
    EmployerCompanyCreateCommand,
    EmployerCompanyDeleteCommand,
    EmployerCompanyLeaveCommand,
    EmployerCompanyListCommand,
    EmployerCompanyRetrieveCommand,
    EmployerCompanyUpdateCommand,
)
from domain.models.companies import Company, CompanyM2MEmployer
from domain.types import TPrimaryKey, TRole
from service_layer.exceptions import PermissionDeniedException, ValidationException
from service_layer.unit_of_work.db import DBUnitOfWork

from ..permissions import has_role


@has_role(role=TRole.EMPLOYER)
async def company_list_handler(
    message: EmployerCompanyListCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> List[Company]:
    return []


@has_role(role=TRole.EMPLOYER)
async def company_create_handler(
    message: EmployerCompanyCreateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> Company:
    async with uow:
        if await uow.users.exists(id=current_user_id, role=TRole.CONTRACTOR):
            raise PermissionDeniedException(detail="Contractor cannot create a company")
        if not message.name:
            raise ValidationException(detail="Empty name")
        if await uow.companies.exists(name=message.name, owner_id=current_user_id):
            raise ValidationException(detail="User already has company with this name")
        company = Company(
            id=uuid4(),
            name=message.name,
            owner_id=current_user_id,
            created_date=datetime.utcnow(),
        )
        company_m2m_employer = CompanyM2MEmployer(
            id=uuid4(),
            company_id=company.id,
            employer_id=current_user_id,
            created_date=datetime.utcnow(),
        )
        await uow.companies.add(company)
        await uow.companies_m2m_employers.add(company_m2m_employer)
        await uow.commit()
    return company


@has_role(role=TRole.EMPLOYER)
async def company_retrieve_handler(
    message: EmployerCompanyRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> Company:
    async with uow:
        if not await uow.companies_m2m_employers.exists(employer_id=current_user_id, company_id=message.company_id):
            raise PermissionDeniedException(detail=f"Employer has no access to company with id {message.company_id}")
        company = await uow.companies.get(id=message.company_id)
    return company


@has_role(role=TRole.EMPLOYER)
async def company_update_handler(
    message: EmployerCompanyUpdateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> List[Company]:
    async with uow:
        if not await uow.companies_m2m_employers.exists(employer_id=current_user_id, company_id=message.company_id):
            raise PermissionDeniedException(detail=f"Employer has no access to company with id {message.company_id}")
        company = await uow.companies.get(id=message.company_id)
        company.name = message.name
        await uow.companies.update(company)
        await uow.commit()
    return company


@has_role(role=TRole.EMPLOYER)
async def company_delete_handler(
    message: EmployerCompanyDeleteCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> List[Company]:
    async with uow:
        if not await uow.companies_m2m_employers.exists(employer_id=current_user_id, company_id=message.company_id):
            raise PermissionDeniedException(detail=f"Employer has no access to company with id {message.company_id}")
        await uow.companies_m2m_employers.delete(company_id=message.company_id, employer_id=current_user_id)
        await uow.companies.delete(message.company_id)
        await uow.commit()


@has_role(role=TRole.EMPLOYER)
async def company_leave_handler(
    message: EmployerCompanyLeaveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
) -> List[Company]:
    async with uow:
        if not await uow.companies_m2m_employers.exists(employer_id=current_user_id, company_id=message.company_id):
            raise PermissionDeniedException(detail=f"Employer has no access to company with id {message.company_id}")
        await uow.companies_m2m_employers.delete(company_id=message.company_id, employer_id=current_user_id)
        await uow.commit()
