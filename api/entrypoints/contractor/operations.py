from typing import List

from fastapi import APIRouter, Depends

from api.domain.types import TPrimaryKey
from bootstrap import bus
from domain.commands.contractor.operations import ContractorOperationListCommand, ContractorOperationRetrieveCommand
from domain.responses.operations import OperationResponse

from ..dependencies import get_current_contractor_pk

router = APIRouter(
    prefix="/contractor/operations",
    tags=["contractor-operations"],
)


@router.get("/", response_model=List[OperationResponse])
async def get_operations(
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Get operations for authenticated contractor."""
    result = await bus.handler(ContractorOperationListCommand(), current_user_pk=current_contractor_pk)
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
