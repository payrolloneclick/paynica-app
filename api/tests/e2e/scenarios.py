import uuid

import jwt
from httpx import AsyncClient

from bootstrap import bus
from domain.models.users import User
from domain.types import TRole
from settings import JWT_SECRET_KEY


async def signup_user(
    async_client: AsyncClient,
    email: str,
    role: TRole,
    password: str,
) -> User:
    response = await async_client.post(
        "/users/signup-user",
        json={
            "email": email,
            "role": role,
            "password": password,
            "repeat_password": password,
        },
    )
    assert response.status_code == 200, response.text
    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]
    assert db_user.email == email
    assert db_user.role == role
    assert await db_user.verify_password(password)
    assert not db_user.is_active
    assert not db_user.is_onboarded
    return db_user


async def signup_verify_email(async_client: AsyncClient, email: str) -> User:
    response = await async_client.post(
        "/users/send-email-code",
        json={
            "email": email,
        },
    )
    assert response.status_code == 200, response.text

    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]
    assert not db_user.is_email_verified
    email_code = db_user.email_code
    response = await async_client.post(
        "/users/verify-email",
        json={
            "email_code": email_code,
        },
    )
    assert response.status_code == 200, response.text
    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]
    assert db_user.is_email_verified
    assert db_user.is_active
    return db_user


async def signup_verify_phone(async_client: AsyncClient, phone: str) -> User:
    response = await async_client.post(
        "/users/send-phone-code",
        json={
            "phone": phone,
        },
    )
    assert response.status_code == 200, response.text

    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]
    assert not db_user.is_phone_verified
    phone_code = db_user.phone_code
    response = await async_client.post(
        "/users/verify-phone",
        json={
            "phone_code": phone_code,
        },
    )
    assert response.status_code == 200, response.text

    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]
    assert db_user.is_phone_verified
    return db_user


async def signin_generate_access_token(async_client: AsyncClient, email: str, password: str) -> dict:
    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 200, response.text
    token_data = response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert "access_token_expired_at" in token_data
    assert "refresh_token_expired_at" in token_data
    decoded_token_data = jwt.decode(token_data["access_token"], JWT_SECRET_KEY, algorithms=["HS256"])
    async with bus.uow:
        user = await bus.uow.users.get(pk=uuid.UUID(decoded_token_data["user_pk"]))
    assert user.email == email
    assert await user.verify_password(password)
    assert decoded_token_data["refresh_token"] == token_data["refresh_token"]
    assert decoded_token_data["access_token_expired_at"] == token_data["access_token_expired_at"]
    assert decoded_token_data["refresh_token_expired_at"] == token_data["refresh_token_expired_at"]
    return token_data


async def signin_refresh_access_token(async_client: AsyncClient, email: str, password: str) -> dict:
    old_token_data = await signin_generate_access_token(async_client, email, password)
    response = await async_client.post(
        "/users/refresh-access-token",
        json={
            "refresh_token": old_token_data["refresh_token"],
        },
    )
    assert response.status_code == 200, response.text
    token_data = response.json()
    assert token_data["access_token"] != old_token_data["access_token"]

    decoded_token_data = jwt.decode(token_data["access_token"], JWT_SECRET_KEY, algorithms=["HS256"])
    async with bus.uow:
        user = await bus.uow.users.get(pk=uuid.UUID(decoded_token_data["user_pk"]))
    assert user.email == email
    assert await user.verify_password(password)
    assert decoded_token_data["access_token_expired_at"] == token_data["access_token_expired_at"]
    assert decoded_token_data["refresh_token"] == old_token_data["refresh_token"]
    assert decoded_token_data["refresh_token_expired_at"] == old_token_data["refresh_token_expired_at"]
    return token_data


async def reset_password(
    async_client: AsyncClient,
    email: str,
    old_password: str,
    new_password: str,
) -> dict:
    response = await async_client.post(
        "/users/send-password-code",
        json={
            "email": email,
        },
    )
    assert response.status_code == 200, response.text
    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]

    assert await db_user.verify_password(old_password)
    assert not await db_user.verify_password(new_password)
    password_code = db_user.password_code
    response = await async_client.post(
        "/users/reset-password",
        json={
            "password_code": password_code,
            "password": new_password,
            "repeat_password": new_password,
        },
    )
    assert response.status_code == 200, response.text

    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]
    assert not await db_user.verify_password(old_password)
    assert await db_user.verify_password(new_password)
    return db_user


async def get_profile(async_client: AsyncClient, email: str, password: str) -> dict:
    response = await signin_generate_access_token(async_client, email, password)
    access_token = response["access_token"]
    response = await async_client.get("/users/profile", headers={"Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    return user_data


async def update_profile(async_client: AsyncClient, email: str, password: str, data: dict) -> dict:
    response = await signin_generate_access_token(async_client, email, password)
    access_token = response["access_token"]
    response = await async_client.patch(
        "/users/profile",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            "email": data.get("email"),
            "phone": data.get("phone"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "password": data.get("password"),
            "repeat_password": data.get("repeat_password"),
        },
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    async with bus.uow:
        db_user = await bus.uow.users.get(pk=uuid.UUID(user_data["pk"]))

    if "email" in data:
        assert not db_user.is_email_verified

    if "phone" in data:
        assert not db_user.is_phone_verified

    for field in ("email", "phone", "first_name", "last_name", "password"):
        if field in data and field != "password":
            assert getattr(db_user, field) == data[field], data[field]
        if field in data and field == "password":
            assert await db_user.verify_password(data[field]), data[field]

    return user_data


async def delete_profile(async_client: AsyncClient, email: str, password: str) -> dict:
    response = await signin_generate_access_token(async_client, email, password)
    access_token = response["access_token"]
    response = await async_client.delete("/users/profile", headers={"Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk",):
        assert field in user_data, field

    async with bus.uow:
        db_user = await bus.uow.users.filter(pk=uuid.UUID(user_data["pk"]))

    assert len(db_user) == 0
    return user_data
