from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic.types import UUID4

from bootstrap import bus
from domain.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    GenerateEmailCodeCommand,
    GeneratePhoneCodeCommand,
    GenerateResetPasswordCodeCommand,
    ResetPasswordCommand,
    RetrieveUserCommand,
    SendEmailCodeByEmailCommand,
    SendPhoneCodeBySmsCommand,
    SendResetPasswordCodeByEmailCommand,
    UpdateUserCommand,
    VerifyEmailCodeCommand,
    VerifyPhoneCodeCommand,
)
from domain.responses.users import UserResponse

from .dependencies import get_current_user_pk

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create-inactive-user", response_model=UserResponse)
async def create_inactive_user(
    command: CreateUserCommand,
):
    """Create inactive user."""
    result = await bus.handler(command)
    return UserResponse(**result.dict())


@router.post("/send-email-code", response_model=UserResponse)
async def send_email_code(
    command: GenerateEmailCodeCommand,
    background_tasks: BackgroundTasks,
):
    """Send email code to verify email."""
    result = await bus.handler(command)
    send_command = SendEmailCodeByEmailCommand(user=result)
    background_tasks.add_task(bus.handler, send_command)
    return UserResponse(**result.dict())


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(
    command: VerifyEmailCodeCommand,
):
    """Verify email."""
    result = await bus.handler(command)
    return UserResponse(**result.dict())


@router.post("/send-phone-code", response_model=UserResponse)
async def send_phone_code(
    command: GeneratePhoneCodeCommand,
    background_tasks: BackgroundTasks,
):
    """Send phone code to verify email."""
    result = await bus.handler(command)
    send_command = SendPhoneCodeBySmsCommand(user=result)
    background_tasks.add_task(bus.handler, send_command)
    return UserResponse(**result.dict())


@router.post("/verify-phone", response_model=UserResponse)
async def verify_phone(
    command: VerifyPhoneCodeCommand,
):
    """Verify phone."""
    result = await bus.handler(command)
    return UserResponse(**result.dict())


@router.post("/send-password-code", response_model=UserResponse)
async def send_password_code(
    command: GenerateResetPasswordCodeCommand,
    background_tasks: BackgroundTasks,
):
    """Send password code to verify email."""
    result = await bus.handler(command)
    send_command = SendResetPasswordCodeByEmailCommand(user=result)
    background_tasks.add_task(bus.handler, send_command)
    return UserResponse(**result.dict())


@router.post("/reset-password", response_model=UserResponse)
async def reset_password(
    command: ResetPasswordCommand,
):
    """Verify password code and reset password."""
    result = await bus.handler(command)
    return UserResponse(**result.dict())


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Get profile of authenticated user."""
    result = await bus.handler(RetrieveUserCommand(pk=current_user_pk), current_user_pk=current_user_pk)
    return UserResponse(**result.dict())


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    command: UpdateUserCommand,
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Update profile of authenticated user."""
    result = await bus.handler(command, current_user_pk=current_user_pk)
    return UserResponse(**result.dict())


@router.delete("/profile", response_model=UserResponse)
async def delete_profile(
    current_user_pk: UUID4 = Depends(get_current_user_pk),
):
    """Delete/inactivate profile of authenticated user."""
    result = await bus.handler(DeleteUserCommand(pk=current_user_pk), current_user_pk=current_user_pk)
    return UserResponse(**result.dict())
