from fastapi import APIRouter, Depends

from .dependencies import token_auth_scheme

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(token_auth_scheme)],
    responses={403: {"description": "Operation forbidden"}, 404: {"description": "Not found"}},
)


@router.post("/sign-up")
async def get_sign_up(user):
    """Get profile of authenticated user."""
    return {"username": "fakecurrentuser"}


@router.get("/profile")
async def get_profile():
    """Get profile of authenticated user."""
    return {"username": "fakecurrentuser"}


@router.patch("/profile")
async def update_profile():
    """Update profile of authenticated user."""
    return {"username": "fakecurrentuser"}


@router.delete("/profile")
async def delete_profile(username: str):
    """Delete/inactivate profile of authenticated user."""
    return {"username": username}


@router.get("/recipients")
async def get_recipients():
    """Get recipients to create an operation."""
    return [{"username": "fakecurrentuser"}]
