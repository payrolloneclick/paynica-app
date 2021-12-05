import pytest

from bootstrap import bus

from .scenarios import (
    get_profile,
    reset_password,
    signin_generate_access_token,
    signin_refresh_access_token,
    signup_create_inactive_user,
    signup_verify_email,
    signup_verify_phone,
)


@pytest.mark.asyncio
async def test_signup(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password", phone="+1 800 444 4444")
    await signup_verify_email(async_client, "test@test.com")
    await signup_verify_phone(async_client, "+1 800 444 4444")


@pytest.mark.asyncio
async def test_generate_access_token(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await signin_generate_access_token(async_client, "test@test.com", "password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_refresh_access_token(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await signin_refresh_access_token(async_client, "test@test.com", "password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_signin_reset_password(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password", phone="+1 800 444 4444")
    await signup_verify_email(async_client, "test@test.com")
    await reset_password(async_client, "test@test.com", "password", "new_password")
    response = await signin_generate_access_token(async_client, "test@test.com", "new_password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_get_profile(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await get_profile(async_client, "test@test.com", "password")
    assert "pk" in response
