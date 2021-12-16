from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

import jwt
from pydantic.types import UUID4

from adapters.email.email import EmailAdapter
from adapters.sms.sms import SmsAdapter
from domain.commands.users import (
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
from domain.models.users import User
from domain.responses.users import GenerateAccessTokenResponse, RefreshAccessTokenResponse
from service_layer.unit_of_work.db import DBUnitOfWork
from settings import JWT_ACCESS_TOKEN_EXPIRED_AT, JWT_REFRESH_TOKEN_EXPIRED_AT, JWT_SECRET_KEY

from ..exceptions import PermissionDeniedException, ValidationException


async def generate_access_token_handler(
    message: GenerateAccessTokenCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> GenerateAccessTokenResponse:
    async with uow:
        user = await uow.users.get(email=message.email)
        if not await user.verify_password(message.password):
            raise PermissionDeniedException("Invalid credentials")

    now = datetime.utcnow()
    refresh_token_expired_at = now + timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRED_AT)
    refresh_token = jwt.encode(
        {
            "user_pk": str(user.pk),
            "refresh_token_expired_at": refresh_token_expired_at.isoformat(),
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )

    access_token_expired_at = now + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRED_AT)
    access_token = jwt.encode(
        {
            "user_pk": str(user.pk),
            "access_token_expired_at": access_token_expired_at.isoformat(),
            "refresh_token": refresh_token,
            "refresh_token_expired_at": refresh_token_expired_at.isoformat(),
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )

    return GenerateAccessTokenResponse(
        access_token=access_token,
        access_token_expired_at=access_token_expired_at,
        refresh_token=refresh_token,
        refresh_token_expired_at=refresh_token_expired_at,
    )


async def refresh_access_token_handler(
    message: RefreshAccessTokenCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> RefreshAccessTokenResponse:
    try:
        decoded_refresh_token = jwt.decode(message.refresh_token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise PermissionDeniedException("Invalid refresh token")

    refresh_token_expired_at = decoded_refresh_token.get("refresh_token_expired_at")
    user_pk = decoded_refresh_token.get("user_pk")
    if not refresh_token_expired_at or not user_pk:
        raise PermissionDeniedException("Invalid payload for refresh token")

    expired_at = datetime.fromisoformat(refresh_token_expired_at)
    now = datetime.utcnow()
    if expired_at < now:
        raise PermissionDeniedException("Expired refresh token")

    async with uow:
        user = await uow.users.get(pk=UUID(user_pk))
        if not user.is_active:
            raise PermissionDeniedException("Inactive user. Please finish sign up process.")
        # TODO get user and salt/token from user to control jwt

    access_token_expired_at = now + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRED_AT)
    access_token = jwt.encode(
        {
            "user_pk": str(user.pk),
            "access_token_expired_at": access_token_expired_at.isoformat(),
            "refresh_token": message.refresh_token,
            "refresh_token_expired_at": refresh_token_expired_at,
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )
    return RefreshAccessTokenResponse(
        access_token=access_token,
        access_token_expired_at=access_token_expired_at,
    )


async def signup_user_handler(
    message: SignUpUserCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    user = User(
        pk=uuid4(),
        email=message.email,
        role=message.role,
        created_date=datetime.now(),
    )
    await user.set_password(message.password)
    async with uow:
        if message.email and await uow.users.exists(email=message.email):
            raise ValidationException(detail="User with this email already exists")
        await uow.users.add(user)
        await uow.commit()
    return user


async def generate_email_code_handler(
    message: GenerateEmailCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(email=message.email)
        if user.is_email_verified:
            raise ValidationException("Email is already verified")
        await user.randomly_set_email_code()
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_email_code_by_email_handler(
    message: SendEmailCodeByEmailCommand,
    email_adapter: Optional[EmailAdapter] = None,
) -> None:
    await email_adapter.send(
        message.user.email,
        "Email verification",
        f"Verification code: {message.user.email_code}",
    )


async def verify_email_code_handler(
    message: VerifyEmailCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(email_code=message.email_code)
        user.is_email_verified = True
        user.is_active = True
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def generate_phone_code_handler(
    message: GeneratePhoneCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(phone=message.phone)
        if user.is_phone_verified:
            raise ValidationException("Phone is already verified")
        await user.randomly_set_phone_code()
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_phone_code_by_sms_handler(
    message: SendPhoneCodeBySmsCommand,
    sms_adapter: Optional[SmsAdapter] = None,
) -> None:
    await sms_adapter.send(
        message.user.phone,
        f"Code: {message.user.phone_code}",
    )


async def verify_phone_code_handler(
    message: VerifyPhoneCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(phone_code=message.phone_code)
        user.is_phone_verified = True
        user.is_active = True
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def generate_reset_password_code_handler(
    message: GenerateResetPasswordCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(email=message.email)
        await user.randomly_set_password_code()
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_reset_password_code_handler(
    message: SendResetPasswordCodeByEmailCommand,
    email_adapter: Optional[EmailAdapter] = None,
    current_user_pk: Optional[UUID4] = None,
) -> None:
    await email_adapter.send(
        message.user.email,
        "Reset password",
        f"Verification code: {message.user.password_code}",
    )


async def reset_password_handler(
    message: ResetPasswordCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> Optional[User]:
    async with uow:
        user = await uow.users.get(password_code=message.password_code)
        await user.set_password(message.password)
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def generate_invitation_code_handler(
    message: GenerateInvitationCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    # TODO
    return


async def send_invitation_code_by_email_handler(
    message: SendInvitationCodeByEmailCommand,
    email_adapter: Optional[EmailAdapter] = None,
) -> None:
    await email_adapter.send(
        message.user.email,
        "Invitation",
        f"Invitation code: {message.user.email_code}",
    )


async def invite_user_handler(
    message: VerifyInvitationCodeAndInviteUserToCompanyCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    # TODO
    return


async def profile_update_handler(
    message: ProfileUpdateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> User:
    async with uow:
        user = await uow.users.get(pk=current_user_pk)
        if message.first_name:
            user.first_name = message.first_name
        if message.last_name:
            user.last_name = message.last_name
        if message.email:
            if await uow.users.exists(email=message.email):
                raise ValidationException(detail="User with this email already exists")
            if message.email != user.email:
                user.is_email_verified = False
            user.email = message.email
        if message.phone:
            if await uow.users.exists(phone=message.phone):
                raise ValidationException(detail="User with this phone already exists")
            if message.phone != user.phone:
                user.is_phone_verified = False
            user.phone = message.phone
        if message.password:
            await user.set_password(message.password)
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def profile_retrieve_handler(
    message: ProfileRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> User:
    async with uow:
        user = await uow.users.get(pk=message.pk, is_active=True)
    return user


async def profile_delete_handler(
    message: ProfileDeleteCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> ProfileDeleteCommand:
    async with uow:
        await uow.users.delete(current_user_pk)
        await uow.commit()
    return message
