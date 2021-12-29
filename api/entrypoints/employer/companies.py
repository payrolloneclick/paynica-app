from typing import List, Optional

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
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_user_id

router = APIRouter(
    prefix="/employer/companies",
    tags=["employer-companies"],
)


@router.get("", response_model=List[CompanyResponse])
async def get_companies(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Get companies list for authenticated employer."""
    command = EmployerCompanyListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(command, current_user_id=current_employer_id)
    return [CompanyResponse(**o.dict()) for o in result]


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Get a company for authenticated employer."""
    command = EmployerCompanyRetrieveCommand(company_id=company_id)
    result = await bus.handler(command, current_user_id=current_employer_id)
    return CompanyResponse(**result.dict())


@router.post("", response_model=CompanyResponse)
async def create_company(
    command: EmployerCompanyCreateCommand,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Create a company for authenticated employer."""
    result = await bus.handler(command, current_user_id=current_employer_id)
    return CompanyResponse(**result.dict())


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: TPrimaryKey,
    command: EmployerCompanyUpdateCommand,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Update a company for authenticated employer."""
    command.company_id = company_id
    result = await bus.handler(command, current_user_id=current_employer_id)
    return CompanyResponse(**result.dict())


@router.delete("/{company_id}")
async def delete_company(
    company_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Delete/inactivate a company for authenticated employer."""
    command = EmployerCompanyDeleteCommand(company_id=company_id)
    await bus.handler(command, current_user_id=current_employer_id)


@router.post("/{company_id}/leave")
async def leave_company(
    company_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Leave a company for authenticated employer."""
    command = EmployerCompanyLeaveCommand(company_id=company_id)
    await bus.handler(command, current_user_id=current_employer_id)
