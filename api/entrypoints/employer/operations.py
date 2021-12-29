from typing import List, Optional

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.employer.operations import EmployerOperationListCommand, EmployerOperationRetrieveCommand
from domain.responses.operations import OperationResponse
from domain.types import TPrimaryKey
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_company_id, get_current_user_id

router = APIRouter(
    prefix="/employer/operations",
    tags=["employer-operations"],
)


@router.get("", response_model=List[OperationResponse])
async def get_operations(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get operations for authenticated employer."""
    command = EmployerOperationListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return [OperationResponse(**o.dict()) for o in result]


@router.get("/{operation_id}", response_model=OperationResponse)
async def get_operation(
    operation_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get an operation for authenticated employer."""
    result = await bus.handler(
        EmployerOperationRetrieveCommand(operation_id=operation_id),
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return OperationResponse(**result.dict())
