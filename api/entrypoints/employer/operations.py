from typing import List

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.employer.operations import EmployerOperationListCommand, EmployerOperationRetrieveCommand
from domain.responses.operations import OperationResponse
from domain.types import TPrimaryKey

from ..dependencies import get_current_employer_pk

router = APIRouter(
    prefix="/employer/operations",
    tags=["employer-operations"],
)


@router.get("/", response_model=List[OperationResponse])
async def get_operations(
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get operations for authenticated employer."""
    result = await bus.handler(EmployerOperationListCommand(), current_user_pk=current_employer_pk)
    return [OperationResponse(**o.dict()) for o in result]


@router.get("/{operation_pk}", response_model=OperationResponse)
async def get_operation(operation_pk: TPrimaryKey, current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk)):
    """Get an operation for authenticated employer."""
    result = await bus.handler(
        EmployerOperationRetrieveCommand(operation_pk=operation_pk), current_user_pk=current_employer_pk
    )
    return OperationResponse(**result.dict())
