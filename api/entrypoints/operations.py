from fastapi import APIRouter, Depends
from pydantic.types import UUID4

from .dependencies import token_auth_scheme

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
    dependencies=[Depends(token_auth_scheme)],
)


@router.get("/operations")
async def get_operations():
    """Get operations for authenticated user."""
    return [{"pk": "uuid4"}]


@router.post("/operations")
async def create_operation():
    """Create an operation for authenticated user."""
    return {"pk": "uuid4"}


@router.get("/operations/{pk}")
async def get_operation(pk: UUID4):
    """Get an operation for authenticated user."""
    return {"pk": "uuid4"}
