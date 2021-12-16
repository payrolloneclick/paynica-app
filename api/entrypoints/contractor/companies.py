from typing import List

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.contractor.companies import (
    ContractorCompanyLeaveCommand,
    ContractorCompanyListCommand,
    ContractorCompanyRetrieveCommand,
)
from domain.responses.companies import CompanyResponse
from domain.types import TPrimaryKey

from ..dependencies import get_current_employer_pk

router = APIRouter(
    prefix="/contractor/companies",
    tags=["contractor-companies"],
)


@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get companies list for authenticated contractor."""
    result = await bus.handler(ContractorCompanyListCommand(), current_user_pk=current_employer_pk)
    return [CompanyResponse(**o.dict()) for o in result]


@router.get("/{company_pk}", response_model=CompanyResponse)
async def get_company(
    company_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get a company for authenticated contractor."""
    command = ContractorCompanyRetrieveCommand(company_pk=company_pk)
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return CompanyResponse(**result.dict())


@router.post("/{company_pk}/leave")
async def leave_company(
    company_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Leave company for authenticated contractor."""
    command = ContractorCompanyLeaveCommand(company_pk=company_pk)
    await bus.handler(command, current_user_pk=current_employer_pk)
