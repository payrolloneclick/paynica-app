from typing import List

from fastapi import APIRouter, Depends
from pydantic.types import UUID4

from bootstrap import bus
from domain.commands.employer.operations import EmployerOperationListCommand, EmployerOperationRetrieveCommand
from domain.responses.operations import OperationResponse

from ..dependencies import get_current_employer_pk

router = APIRouter(
    prefix="/employer/operations",
    tags=["employer-operations"],
)


@router.get("/", response_model=List[OperationResponse])
async def get_operations(
    current_employer_pk: UUID4 = Depends(get_current_employer_pk),
):
    """Get operations for authenticated employer."""
    result = await bus.handler(EmployerOperationListCommand(), current_user_pk=current_employer_pk)
    return [OperationResponse(**o.dict()) for o in result]


@router.get("/{pk}", response_model=OperationResponse)
async def get_operation(pk: UUID4, current_employer_pk: UUID4 = Depends(get_current_employer_pk)):
    """Get an operation for authenticated employer."""
    result = await bus.handler(EmployerOperationRetrieveCommand(pk=pk), current_user_pk=current_employer_pk)
    return OperationResponse(**result.dict())
