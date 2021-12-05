from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

import jwt
from pydantic.types import UUID4

from adapters.email.email import EmailAdapter
from adapters.sms.sms import SmsAdapter
from domain.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    GenerateAccessTokenCommand,
    GenerateEmailCodeCommand,
    GeneratePhoneCodeCommand,
    GenerateResetPasswordCodeCommand,
    RefreshAccessTokenCommand,
    ResetPasswordCommand,
    RetrieveUserCommand,
    SendEmailCodeByEmailCommand,
    SendPhoneCodeBySmsCommand,
    SendResetPasswordCodeByEmailCommand,
    UpdateUserCommand,
    VerifyEmailCodeCommand,
    VerifyPhoneCodeCommand,
)
from domain.models.users import User
from domain.responses.users import GenerateAccessTokenResponse, RefreshAccessTokenResponse
from service_layer.unit_of_work.db import DBUnitOfWork
from settings import JWT_ACCESS_TOKEN_EXPIRED_AT, JWT_REFRESH_TOKEN_EXPIRED_AT, JWT_SECRET_KEY

from ..exceptions import PermissionDeniedException


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

    access_token_expired_at = now + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRED_AT)
    access_token = jwt.encode(
        {
            "user_pk": user_pk,
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


async def create_user_handler(
    message: CreateUserCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    user = User(
        pk=uuid4(),
        email=message.email,
        phone=message.phone,
        first_name=message.first_name,
        last_name=message.last_name,
        created_date=datetime.now(),
    )
    await user.set_password(message.password)
    async with uow:
        await uow.users.add(user)
        await uow.commit()
    return user


async def generate_email_code_handler(
    message: GenerateEmailCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(email=message.email)
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


async def update_user_handler(
    message: UpdateUserCommand,
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
            user.email = message.email
        if message.phone:
            user.phone = message.phone
        if message.password:
            await user.set_password(message.password)
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def retrieve_user_handler(
    message: RetrieveUserCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> User:
    async with uow:
        user = await uow.users.get(pk=message.pk, is_active=True)
    return user


async def delete_user_handler(
    message: DeleteUserCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[UUID4] = None,
) -> DeleteUserCommand:
    async with uow:
        if message.pk != current_user_pk:
            raise PermissionDeniedException(detail="User doesn't have permissions to delete this user")
        await uow.users.delete(message.pk)
        await uow.commit()
    return message
