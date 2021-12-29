from typing import List, Optional

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.contractor.operations import ContractorOperationListCommand, ContractorOperationRetrieveCommand
from domain.responses.operations import OperationResponse
from domain.types import TPrimaryKey
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_company_id, get_current_user_id

router = APIRouter(
    prefix="/contractor/operations",
    tags=["contractor-operations"],
)


@router.get("", response_model=List[OperationResponse])
async def get_operations(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get operations for authenticated contractor."""
    command = ContractorOperationListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(
        command,
        current_user_id=current_contractor_id,
        current_company_id=current_company_id,
    )
    return [OperationResponse(**o.dict()) for o in result]


@router.get("/{operation_id}", response_model=OperationResponse)
async def get_operation(
    operation_id: TPrimaryKey,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get an operation for authenticated contractor."""
    result = await bus.handler(
        ContractorOperationRetrieveCommand(operation_id=operation_id),
        current_user_id=current_contractor_id,
        current_company_id=current_company_id,
    )
    return OperationResponse(**result.dict())
