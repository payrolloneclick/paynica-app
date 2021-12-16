from typing import List

from fastapi import APIRouter, Depends
from pydantic.types import UUID4

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
    current_contractor_pk: UUID4 = Depends(get_current_contractor_pk),
):
    """Get operations for authenticated contractor."""
    result = await bus.handler(ContractorOperationListCommand(), current_user_pk=current_contractor_pk)
    return [OperationResponse(**o.dict()) for o in result]


@router.get("/{pk}", response_model=OperationResponse)
async def get_operation(pk: UUID4, current_contractor_pk: UUID4 = Depends(get_current_contractor_pk)):
    """Get an operation for authenticated contractor."""
    result = await bus.handler(ContractorOperationRetrieveCommand(pk=pk), current_user_pk=current_contractor_pk)
    return OperationResponse(**result.dict())
