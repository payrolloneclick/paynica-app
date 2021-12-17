from typing import List, Optional

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.contractor.operations import ContractorOperationListCommand, ContractorOperationRetrieveCommand
from domain.responses.operations import OperationResponse
from domain.types import TPrimaryKey, TSortByDirection
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_contractor_pk

router = APIRouter(
    prefix="/contractor/operations",
    tags=["contractor-operations"],
)


@router.get("/", response_model=List[OperationResponse])
async def get_operations(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by_field: Optional[str] = None,
    sort_by_direction: Optional[TSortByDirection] = TSortByDirection.DESC,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Get operations for authenticated contractor."""
    command = ContractorOperationListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by_field = sort_by_field
    command.sort_by_direction = sort_by_direction
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return [OperationResponse(**o.dict()) for o in result]


@router.get("/{operation_pk}", response_model=OperationResponse)
async def get_operation(
    operation_pk: TPrimaryKey, current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk)
):
    """Get an operation for authenticated contractor."""
    result = await bus.handler(
        ContractorOperationRetrieveCommand(operation_pk=operation_pk), current_user_pk=current_contractor_pk
    )
    return OperationResponse(**result.dict())
