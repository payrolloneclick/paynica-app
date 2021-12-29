from typing import List, Optional

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.contractor.companies import (
    ContractorCompanyLeaveCommand,
    ContractorCompanyListCommand,
    ContractorCompanyRetrieveCommand,
)
from domain.responses.companies import CompanyResponse
from domain.types import TPrimaryKey
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_user_id

router = APIRouter(
    prefix="/contractor/companies",
    tags=["contractor-companies"],
)


@router.get("", response_model=List[CompanyResponse])
async def get_companies(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Get companies list for authenticated contractor."""
    command = ContractorCompanyListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(command, current_user_id=current_contractor_id)
    return [CompanyResponse(**o.dict()) for o in result]


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: TPrimaryKey,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Get a company for authenticated contractor."""
    command = ContractorCompanyRetrieveCommand(company_id=company_id)
    result = await bus.handler(command, current_user_id=current_contractor_id)
    return CompanyResponse(**result.dict())


@router.post("/{company_id}/leave")
async def leave_company(
    company_id: TPrimaryKey,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
):
    """Leave company for authenticated contractor."""
    command = ContractorCompanyLeaveCommand(company_id=company_id)
    await bus.handler(command, current_user_id=current_contractor_id)
