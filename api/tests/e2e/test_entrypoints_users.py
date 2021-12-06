import pytest

from bootstrap import bus

from .scenarios import (
    delete_profile,
    get_profile,
    reset_password,
    signin_generate_access_token,
    signin_refresh_access_token,
    signup_create_inactive_user,
    signup_verify_email,
    signup_verify_phone,
    update_profile,
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
async def test_signin_reset_password_4xx(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password", phone="+1 800 444 4444")
    await signup_verify_email(async_client, "test@test.com")
    response = await async_client.post(
        "/users/send-password-code",
        json={
            "email": "invalid_email",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/send-password-code",
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/send-password-code",
        json={
            "email": "test@test.com",
        },
    )
    assert response.status_code == 200, response.text
    async with bus.uow:
        db_users = await bus.uow.users.all()
        db_user = db_users[-1]

    password_code = db_user.password_code
    response = await async_client.post(
        "/users/reset-password",
        json={
            "password_code": "invalid_code",
            "password": "new_password",
            "repeat_password": "new_password",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/reset-password",
        json={
            "password_code": "a" * 16,
            "password": "new_password",
            "repeat_password": "new_password",
        },
    )
    assert response.status_code == 404, response.text

    password_code = db_user.password_code
    response = await async_client.post(
        "/users/reset-password",
        json={
            "password_code": password_code,
            "password": "new_password",
            "repeat_password": "new_invalid_password",
        },
    )
    assert response.status_code == 422, response.text

    password_code = db_user.password_code
    response = await async_client.post(
        "/users/reset-password",
        json={
            "password_code": password_code,
            "password": "",
            "repeat_password": "",
        },
    )
    assert response.status_code == 422, response.text

    password_code = db_user.password_code
    response = await async_client.post(
        "/users/reset-password",
        json={
            "password_code": password_code,
            "password": "new_password",
            "repeat_password": "",
        },
    )
    assert response.status_code == 422, response.text

    password_code = db_user.password_code
    response = await async_client.post(
        "/users/reset-password",
        json={
            "password_code": password_code,
            "password": "",
            "repeat_password": "new_password",
        },
    )
    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_get_profile(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await get_profile(async_client, "test@test.com", "password")
    assert "pk" in response


@pytest.mark.asyncio
async def test_get_profile_4xx(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")

    response = await async_client.get("/users/profile")
    assert response.status_code == 403, response.text

    response = await async_client.get(
        "/users/profile", headers={"Authorization": "Bearer {}".format("invalid_access_token")}
    )
    assert response.status_code == 401, response.text


@pytest.mark.asyncio
async def test_update_profile(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")
    await update_profile(
        async_client,
        "test@test.com",
        "password",
        {
            "email": "new_test@test.com",
            "phone": "+1 800 444 4441",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "password": "new_password",
            "repeat_password": "new_password",
        },
    )


@pytest.mark.asyncio
async def test_update_profile_4xx(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")

    data = {
        "email": "new_test@test.com",
        "phone": "+1 800 444 4441",
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "password": "new_password",
        "repeat_password": "new_password",
    }

    response = await async_client.patch(
        "/users/profile",
        json=data,
    )
    assert response.status_code == 403, response.text

    response = await async_client.patch(
        "/users/profile",
        headers={"Authorization": "Bearer {}".format("invalid_access_token")},
        json=data,
    )
    assert response.status_code == 401, response.text

    response = await signin_generate_access_token(async_client, "test@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.patch(
        "/users/profile",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            **data,
            "email": "invalid_email",
        },
    )
    assert response.status_code == 422, response.text

    response = await signin_generate_access_token(async_client, "test@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.patch(
        "/users/profile",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            **data,
            "phone": "invalid_phone",
        },
    )
    assert response.status_code == 422, response.text

    response = await signin_generate_access_token(async_client, "test@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.patch(
        "/users/profile",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            **data,
            "password": "new_password",
            "repeat_password": "invalid_password",
        },
    )
    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_delete_profile(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")
    await delete_profile(
        async_client,
        "test@test.com",
        "password",
    )


@pytest.mark.asyncio
async def test_delete_profile_4xx(async_client):
    await bus.clean()
    await signup_create_inactive_user(async_client, "test@test.com", "password")
    await signup_verify_email(async_client, "test@test.com")

    response = await async_client.delete("/users/profile")
    assert response.status_code == 403, response.text

    response = await async_client.delete(
        "/users/profile", headers={"Authorization": "Bearer {}".format("invalid_access_token")}
    )
    assert response.status_code == 401, response.text
