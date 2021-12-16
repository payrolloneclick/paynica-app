from fastapi import APIRouter, BackgroundTasks, Depends, Response

from bootstrap import bus
from domain.commands.users import (
    ChangePasswordCommand,
    GenerateAccessTokenCommand,
    GenerateEmailCodeCommand,
    GenerateInvitationCodeCommand,
    GeneratePhoneCodeCommand,
    GenerateResetPasswordCodeCommand,
    ProfileDeleteCommand,
    ProfileRetrieveCommand,
    ProfileUpdateCommand,
    RefreshAccessTokenCommand,
    ResetPasswordCommand,
    SendEmailCodeByEmailCommand,
    SendInvitationCodeByEmailCommand,
    SendPhoneCodeBySmsCommand,
    SendResetPasswordCodeByEmailCommand,
    SignUpUserCommand,
    VerifyEmailCodeCommand,
    VerifyInvitationCodeAndInviteUserToCompanyCommand,
    VerifyPhoneCodeCommand,
)
from domain.responses.users import GenerateAccessTokenResponse, RefreshAccessTokenResponse, UserResponse
from domain.types import TPrimaryKey

from .dependencies import get_current_user_pk

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/generate-access-token", response_model=GenerateAccessTokenResponse)
async def generate_access_token(
    response: Response,
    command: GenerateAccessTokenCommand,
):
    """Generate access token."""
    result = await bus.handler(command)
    response.set_cookie(key="access_token", value=f"Bearer {result.access_token}", httponly=True)
    response.set_cookie(key="refresh_token", value=f"Bearer {result.refresh_token}", httponly=True)
    return GenerateAccessTokenResponse(**result.dict())


@router.post("/refresh-access-token", response_model=RefreshAccessTokenResponse)
async def refresh_access_token(
    command: RefreshAccessTokenCommand,
):
    """Refresh access token."""
    result = await bus.handler(command)
    return RefreshAccessTokenResponse(**result.dict())


@router.post("/signup-user")
async def signup_user(
    command: SignUpUserCommand,
):
    """Signup user."""
    await bus.handler(command)


@router.post("/send-email-code")
async def send_email_code(
    command: GenerateEmailCodeCommand,
    background_tasks: BackgroundTasks,
):
    """Send email code to verify email."""
    result = await bus.handler(command)
    send_command = SendEmailCodeByEmailCommand(user=result)
    background_tasks.add_task(bus.handler, send_command)


@router.post("/verify-email")
async def verify_email(
    command: VerifyEmailCodeCommand,
):
    """Verify email."""
    await bus.handler(command)


@router.post("/send-phone-code")
async def send_phone_code(
    command: GeneratePhoneCodeCommand,
    background_tasks: BackgroundTasks,
):
    """Send phone code to verify email."""
    result = await bus.handler(command)
    send_command = SendPhoneCodeBySmsCommand(user=result)
    background_tasks.add_task(bus.handler, send_command)


@router.post("/verify-phone")
async def verify_phone(
    command: VerifyPhoneCodeCommand,
):
    """Verify phone."""
    await bus.handler(command)


@router.post("/send-password-code")
async def send_password_code(
    command: GenerateResetPasswordCodeCommand,
    background_tasks: BackgroundTasks,
):
    """Send password code to verify email."""
    result = await bus.handler(command)
    send_command = SendResetPasswordCodeByEmailCommand(user=result)
    background_tasks.add_task(bus.handler, send_command)


@router.post("/reset-password")
async def reset_password(
    command: ResetPasswordCommand,
):
    """Verify password code and reset password."""
    await bus.handler(command)


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Get profile of authenticated user."""
    result = await bus.handler(ProfileRetrieveCommand(), current_user_pk=current_user_pk)
    return UserResponse(**result.dict())


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    command: ProfileUpdateCommand,
    current_user_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Update profile of authenticated user."""
    result = await bus.handler(command, current_user_pk=current_user_pk)
    return UserResponse(**result.dict())


@router.delete("/profile")
async def delete_profile(
    current_user_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Delete/inactivate profile of authenticated user."""
    await bus.handler(ProfileDeleteCommand(), current_user_pk=current_user_pk)


@router.patch("/change-password", response_model=UserResponse)
async def change_password(
    command: ChangePasswordCommand,
    current_user_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Change password of authenticated user."""
    result = await bus.handler(command, current_user_pk=current_user_pk)
    return UserResponse(**result.dict())


@router.post("/send-invitation-code")
async def send_invitation_code(
    command: GenerateInvitationCodeCommand,
    background_tasks: BackgroundTasks,
    current_user_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Send email code to verify email."""
    result = await bus.handler(command, current_user_pk=current_user_pk)
    send_command = SendInvitationCodeByEmailCommand(invite_user_to_company=result)
    background_tasks.add_task(bus.handler, send_command)


@router.post("/invite-user")
async def invite_user(
    command: VerifyInvitationCodeAndInviteUserToCompanyCommand,
):
    """Invite user."""
    await bus.handler(command)
