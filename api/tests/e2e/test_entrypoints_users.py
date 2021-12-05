import pytest

from bootstrap import bus

from .scenarios import (
    signin_generate_access_token,
    signin_refresh_access_token,
    signup_create_inactive_user,
    signup_verify_email,
    signup_verify_phone,
    get_profile,
)


@pytest.mark.asyncio
async def test_signup(async_client):
    await bus.clean()
    response = await signup_create_inactive_user(async_client, "test@test.com", "password")
    response = await signup_verify_email(async_client, response["email"])
    response = await signup_verify_phone(async_client, response["phone"])
    assert "pk" in response


@pytest.mark.asyncio
async def test_generate_access_token(async_client):
    await bus.clean()
    response = await signin_generate_access_token(async_client, "test@test.com", "password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_refresh_access_token(async_client):
    await bus.clean()
    response = await signin_refresh_access_token(async_client, "test@test.com", "password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_get_profile(async_client):
    await bus.clean()
    response = await signin_generate_access_token(async_client, "test@test.com", "password")
    access_token = response["access_token"]
    response = await get_profile(async_client, access_token)
