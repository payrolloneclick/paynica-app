from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic.types import UUID4

from api.adapters.email.generic import AbstractEmailAdapter
from api.adapters.sms.generic import AbstractSmsAdapter
from api.domain.models.users import User

from ..unit_of_work.generic import AbstractUnitOfWork


async def create_user(
    uow: AbstractUnitOfWork,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    password: str,
) -> User:
    user = User(
        pk=uuid4(), email=email, phone=phone, first_name=first_name, last_name=last_name, created_date=datetime.now()
    )
    user.set_password_hash(password)
    async with uow:
        await uow.users.add(user)
        await uow.commit()
    return user


async def save_phone_code_for_phone(
    uow: AbstractUnitOfWork,
    phone: str,
) -> Optional[User]:
    user = None
    async with uow:
        users = await uow.users.filter(phone)
        if not users:
            return user
        user = users[0]
        await user.randomly_set_phone_code()
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_phone_code_by_sms(
    sms_adapter: AbstractSmsAdapter,
    user: User,
) -> bool:
    if not user.phone:
        return False
    await sms_adapter.send(user.phone, f"Code: {user.phone_code}")
    return True


async def verify_phone_code(
    uow: AbstractUnitOfWork,
    phone_code: str,
) -> Optional[User]:
    user = None
    async with uow:
        users = await uow.users.filter(phone_code=phone_code)
        if not users:
            return user
        user = users[0]
        user.is_phone_verified = True
        user.is_active = True
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def save_email_code_for_email(
    uow: AbstractUnitOfWork,
    email: str,
) -> Optional[User]:
    user = None
    async with uow:
        users = await uow.users.filter(email)
        if not users:
            return user
        user = users[0]
        await user.randomly_set_email_code()
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_email_code_by_email(
    email_adapter: AbstractEmailAdapter,
    user: User,
) -> None:
    if not user.email:
        return False
    await email_adapter.send(user.email, "Email verification", f"Verification code: {user.email_code}")
    return True


async def verify_email_code(
    uow: AbstractUnitOfWork,
    email_code: str,
) -> Optional[User]:
    user = None
    async with uow:
        users = await uow.users.filter(email_code=email_code)
        if not users:
            return user
        user = users[0]
        user.is_email_verified = True
        user.is_active = True
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def save_password_code_for_email(
    uow: AbstractUnitOfWork,
    email: str,
) -> Optional[User]:
    user = None
    async with uow:
        users = await uow.users.filter(email=email)
        if not users:
            return user
        user = users[0]
        await user.randomly_set_password_code()
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_password_code_by_email(
    email_adapter: AbstractEmailAdapter,
    user: User,
) -> None:
    if not user.email:
        return False
    await email_adapter.send(user.email, "Reset password", f"Verification code: {user.password_code}")
    return True


async def verify_password_code_and_reset_password(
    uow: AbstractUnitOfWork,
    password_code: str,
    password: str,
) -> Optional[User]:
    user = None
    async with uow:
        users = await uow.users.filter(password_code=password_code)
        if not users:
            return user
        user = users[0]
        await user.set_password_hash(password)
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def update_user(
    uow: AbstractUnitOfWork,
    pk: UUID4,
    first_name: Optional(str) = None,
    last_name: Optional(str) = None,
    email: Optional(str) = None,
    phone: Optional(str) = None,
    password: Optional(str) = None,
) -> Optional[User]:
    user = None
    async with uow:
        user = await uow.users.get(pk)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        if password:
            await user.set_password_hash(password)
        user.updated_date = datetime.now()
        await uow.users.update(user)
        await uow.commit()
    return user


async def get_active_user(
    uow: AbstractUnitOfWork,
    pk: UUID4,
) -> Optional[User]:
    user = None
    async with uow:
        user = await uow.users.get(pk)
        if not user.is_active:
            return None
    return user


async def delete_user(
    uow: AbstractUnitOfWork,
    pk: UUID4,
) -> UUID4:
    async with uow:
        await uow.users.delete(pk)
        await uow.commit()
    return pk
