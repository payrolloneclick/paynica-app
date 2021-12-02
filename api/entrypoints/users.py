from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic.types import UUID4

from service_layer.services import users as users_services
from bootstrap import sms_adapter, email_adapter, uow

from .dependencies import get_current_user_pk
from .schemas.users import (
    UserCreateRequest,
    UserEmailCodeRequest,
    UserEmailRequest,
    UserPhoneCodeRequest,
    UserPhoneRequest,
    UserPresetPasswordRequest,
    UserResponse,
    UserUpdateRequest,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/create-inactive-user", response_model=UserResponse)
async def create_inactive_user(
    body: UserCreateRequest,
):
    """Create inactive user."""
    user = await users_services.create_user(
        uow,
        **body.dict(exclude_unset=True, exclude_none=True, exclude=set(["repeat_password"])),
    )
    return UserResponse(**user.dict())


@router.post("/send-email-code", response_model=UserResponse)
async def send_email_code(
    body: UserEmailRequest,
    background_tasks: BackgroundTasks,
):
    """Send email code to verify email."""
    user = await users_services.save_email_code_for_email(uow, body.email)
    background_tasks.add_task(users_services.send_email_code_by_email, email_adapter=email_adapter, user=user)
    return UserResponse(**user.dict())


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(
    body: UserEmailCodeRequest,
):
    """Verify email."""
    user = await users_services.verify_email_code(uow, body.email_code)
    return UserResponse(**user.dict())


@router.post("/send-phone-code", response_model=UserResponse)
async def send_phone_code(
    body: UserPhoneRequest,
    background_tasks: BackgroundTasks,
):
    """Send phone code to verify email."""
    user = await users_services.save_phone_code_for_phone(uow, body.phone)
    background_tasks.add_task(users_services.send_phone_code_by_sms, sms_adapter=sms_adapter, user=user)
    return UserResponse(**user.dict())


@router.post("/verify-phone", response_model=UserResponse)
async def verify_phone(
    body: UserPhoneCodeRequest,
):
    """Verify phone."""
    user = await users_services.verify_phone_code(uow, body.phone_code)
    return UserResponse(**user.dict())


@router.post("/send-password-code", response_model=UserResponse)
async def send_password_code(
    body: UserEmailRequest,
    background_tasks: BackgroundTasks,
):
    """Send password code to verify email."""
    user = await users_services.save_password_code_for_email(uow, body.email)
    background_tasks.add_task(users_services.send_password_code_by_email, email_adapter=email_adapter, user=user)
    return UserResponse(**user.dict())


@router.post("/reset-password", response_model=UserResponse)
async def reset_password(
    body: UserPresetPasswordRequest,
):
    """Verify password code and reset password."""
    user = await users_services.verify_password_code_and_reset_password(
        uow, **body.dict(exclude_unset=True, exclude_none=True)
    )
    return UserResponse(**user.dict())


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Get profile of authenticated user."""
    user = await users_services.get_active_user(uow, current_user_pk)
    return UserResponse(**user.dict())


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    body: UserUpdateRequest,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Update profile of authenticated user."""
    user = await users_services.update_user(uow, current_user_pk, **body.dict(exclude_unset=True, exclude_none=True))
    return UserResponse(**user.dict())


@router.delete("/profile")
async def delete_profile(
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Delete/inactivate profile of authenticated user."""
    pk = await users_services.delete_user(uow, current_user_pk)
    return pk
