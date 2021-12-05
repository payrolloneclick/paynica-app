import uuid
from typing import Optional

import jwt
from httpx import AsyncClient

from bootstrap import bus
from settings import JWT_SECRET_KEY


async def signup_create_inactive_user(
    async_client: AsyncClient,
    email: str,
    password: str,
    phone: Optional[str] = "+1 800 444 4444",
    first_name: Optional[str] = "test first name",
    last_name: Optional[str] = "test last name",
) -> dict:
    response = await async_client.post(
        "/users/create-inactive-user",
        json={
            "email": email,
            "phone": phone,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "repeat_password": password,
        },
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    return user_data


async def signup_verify_email(async_client: AsyncClient, email: str) -> dict:
    response = await async_client.post(
        "/users/send-email-code",
        json={
            "email": email,
        },
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    async with bus.uow:
        db_user = await bus.uow.users.get(pk=uuid.UUID(user_data["pk"]))
    assert not db_user.is_email_verified
    email_code = db_user.email_code
    response = await async_client.post(
        "/users/verify-email",
        json={
            "email_code": email_code,
        },
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    async with bus.uow:
        db_user = await bus.uow.users.get(pk=uuid.UUID(user_data["pk"]))
    assert db_user.is_email_verified
    return user_data


async def signup_verify_phone(async_client: AsyncClient, phone: str) -> dict:
    response = await async_client.post(
        "/users/send-phone-code",
        json={
            "phone": phone,
        },
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    async with bus.uow:
        db_user = await bus.uow.users.get(pk=uuid.UUID(user_data["pk"]))
    assert not db_user.is_phone_verified
    phone_code = db_user.phone_code
    response = await async_client.post(
        "/users/verify-phone",
        json={
            "phone_code": phone_code,
        },
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    async with bus.uow:
        db_user = await bus.uow.users.get(pk=uuid.UUID(user_data["pk"]))
    assert db_user.is_phone_verified
    return user_data


async def signin_generate_access_token(async_client: AsyncClient, email: str, password: str) -> dict:
    response = await signup_create_inactive_user(async_client, "test@test.com", "password")
    response = await signup_verify_email(async_client, response["email"])
    response = await signup_verify_phone(async_client, response["phone"])
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
    assert user.verify_password(password)
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
    assert user.verify_password(password)
    assert decoded_token_data["access_token_expired_at"] == token_data["access_token_expired_at"]
    assert decoded_token_data["refresh_token"] == old_token_data["refresh_token"]
    assert decoded_token_data["refresh_token_expired_at"] == old_token_data["refresh_token_expired_at"]
    return token_data


async def get_profile(async_client: AsyncClient, access_token: str) -> dict:
    response = await async_client.get(
        "/users/profile",
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    for field in ("pk", "email", "phone", "first_name", "last_name"):
        assert field in user_data, field

    return user_data