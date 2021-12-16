from typing import List

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.employer.companies import (
    EmployerCompanyCreateCommand,
    EmployerCompanyDeleteCommand,
    EmployerCompanyLeaveCommand,
    EmployerCompanyListCommand,
    EmployerCompanyRetrieveCommand,
    EmployerCompanyUpdateCommand,
)
from domain.responses.companies import CompanyResponse
from domain.types import TPrimaryKey

from ..dependencies import get_current_employer_pk

router = APIRouter(
    prefix="/employer/companies",
    tags=["employer-companies"],
)


@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get companies list for authenticated employer."""
    result = await bus.handler(EmployerCompanyListCommand(), current_user_pk=current_employer_pk)
    return [CompanyResponse(**o.dict()) for o in result]


@router.get("/{company_pk}", response_model=CompanyResponse)
async def get_company(
    company_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get a company for authenticated employer."""
    command = EmployerCompanyRetrieveCommand(company_pk=company_pk)
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return CompanyResponse(**result.dict())


@router.post("/", response_model=CompanyResponse)
async def create_company(
    command: EmployerCompanyCreateCommand,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Create a company for authenticated employer."""
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return CompanyResponse(**result.dict())


@router.patch("/{company_pk}", response_model=CompanyResponse)
async def update_company(
    company_pk: TPrimaryKey,
    command: EmployerCompanyUpdateCommand,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Update a company for authenticated employer."""
    command.company_pk = company_pk
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return CompanyResponse(**result.dict())


@router.delete("/{company_pk}")
async def delete_company(
    company_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Delete/inactivate a company for authenticated employer."""
    command = EmployerCompanyDeleteCommand(company_pk=company_pk)
    await bus.handler(command, current_user_pk=current_employer_pk)


@router.post("/{company_pk}/leave")
async def leave_company(
    company_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Leave a company for authenticated employer."""
    command = EmployerCompanyLeaveCommand(company_pk=company_pk)
    await bus.handler(command, current_user_pk=current_employer_pk)
