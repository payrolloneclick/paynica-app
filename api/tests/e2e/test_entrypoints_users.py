import pytest

from bootstrap import bus
from domain.types import TRole

from .scenarios import (
    delete_profile,
    get_profile,
    reset_password,
    signin_generate_access_token,
    signin_refresh_access_token,
    signup_user,
    signup_verify_email,
    signup_verify_phone,
    update_profile,
)


@pytest.mark.asyncio
async def test_signup(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")


@pytest.mark.asyncio
async def test_signup_4xx(async_client):
    url = "/users/signup-user"

    response = await async_client.post(
        url,
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        url,
        json={
            "email": "test@test.com",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        url,
        json={
            "email": "test@test.com",
            "role": TRole.EMPLOYER,
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        url,
        json={
            "email": "test@test.com",
            "role": TRole.EMPLOYER,
            "password": "password",
        },
    )
    assert response.status_code == 422, response.text

    data = {
        "email": "test@test.com",
        "role": TRole.EMPLOYER,
        "password": "password",
        "repeat_password": "password",
    }
    response = await async_client.post(
        url,
        json={
            **data,
            "email": "invalid_email",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        url,
        json={
            **data,
            "role": "invalid_role",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        url,
        json={
            **data,
            "repeat_password": "invalid_password",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        url,
        json=data,
    )
    assert response.status_code == 200, response.text
    assert response.json() is None

    response = await async_client.post(
        url,
        json={
            **data,
            "role": TRole.CONTRACTOR,
        },
    )
    # email duplication
    assert response.status_code == 400, response.text


@pytest.mark.asyncio
async def test_signup_verify_email_4xx(async_client):
    send_email_code_url = "/users/send-email-code"
    verify_email_url = "/users/verify-email"
    await signup_user(async_client, "active_test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "active_test@test.com")

    await signup_user(async_client, "test@test.com", TRole.CONTRACTOR, "password")

    response = await async_client.post(
        send_email_code_url,
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        send_email_code_url,
        json={
            "email": "",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        send_email_code_url,
        json={
            "email": "active_test@test.com",
        },
    )
    assert response.status_code == 400, response.text

    response = await async_client.post(
        send_email_code_url,
        json={
            "email": "test@test.com",
        },
    )
    assert response.status_code == 200, response.text

    response = await async_client.post(
        verify_email_url,
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        verify_email_url,
        json={
            "email_code": "",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        verify_email_url,
        json={
            "email_code": "invalid_code",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        verify_email_url,
        json={
            "email_code": "a" * 16,
        },
    )
    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test_signup_verify_phone_4xx(async_client):
    send_phone_code_url = "/users/send-phone-code"
    verify_phone_url = "/users/verify-phone"
    db_user = await signup_user(async_client, "active_test@test.com", TRole.EMPLOYER, "password")
    async with bus.uow:
        db_user.phone = "+1 800 444 4440"
        await bus.uow.users.update(db_user)
    await signup_verify_phone(async_client, "+1 800 444 4440")

    db_user = await signup_user(
        async_client,
        "test@test.com",
        TRole.CONTRACTOR,
        "password",
    )
    async with bus.uow:
        db_user.phone = "+1 800 444 4444"
        await bus.uow.users.update(db_user)

    response = await async_client.post(
        send_phone_code_url,
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        send_phone_code_url,
        json={
            "phone": "",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        send_phone_code_url,
        json={
            "phone": "+1 800 444 4440",  # already verified
        },
    )
    assert response.status_code == 400, response.text

    response = await async_client.post(
        send_phone_code_url,
        json={
            "phone": "+1 800 444 4444",
        },
    )
    assert response.status_code == 200, response.text

    response = await async_client.post(
        verify_phone_url,
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        verify_phone_url,
        json={
            "phone_code": "",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        verify_phone_url,
        json={
            "phone_code": "a",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        verify_phone_url,
        json={
            "phone_code": "a" * 6,
        },
    )
    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test_generate_access_token(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await signin_generate_access_token(async_client, "test@test.com", "password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_generate_access_token_4xx(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await async_client.post(
        "/users/generate-access-token",
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "email": "test@test.com",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "password": "password",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "email": "",
            "password": "password",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "email": "test@test.com",
            "password": "",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "email": "invalid",
            "password": "password",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "email": "wrong@email.com",
            "password": "password",
        },
    )
    assert response.status_code == 404, response.text

    response = await async_client.post(
        "/users/generate-access-token",
        json={
            "email": "test@test.com",
            "password": "wrong_password",
        },
    )
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_refresh_access_token(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await signin_refresh_access_token(async_client, "test@test.com", "password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_refresh_access_token_4xx(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")
    await signin_generate_access_token(async_client, "test@test.com", "password")
    response = await async_client.post(
        "/users/refresh-access-token",
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/refresh-access-token",
        json={
            "refresh_token": "",
        },
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        "/users/refresh-access-token",
        json={
            "refresh_token": "invalid_token",
        },
    )
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_signin_reset_password(async_client):
    await signup_user(async_client, "test@test.com", "password", phone="+1 800 444 4444")
    await signup_verify_email(async_client, "test@test.com")
    await reset_password(async_client, "test@test.com", "password", "new_password")
    response = await signin_generate_access_token(async_client, "test@test.com", "new_password")
    assert "access_token" in response


@pytest.mark.asyncio
async def test_signin_reset_password_4xx(async_client):
    await signup_user(async_client, "test@test.com", "password", phone="+1 800 444 4444")
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
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")
    response = await get_profile(async_client, "test@test.com", "password")
    assert "pk" in response


@pytest.mark.asyncio
async def test_get_profile_4xx(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")

    response = await async_client.get("/users/profile")
    assert response.status_code == 403, response.text

    response = await async_client.get(
        "/users/profile", headers={"Authorization": "Bearer {}".format("invalid_access_token")}
    )
    assert response.status_code == 401, response.text


@pytest.mark.asyncio
async def test_update_profile(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
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
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
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

    await signup_user(async_client, "another_test@test.com", "password", phone="+1 800 444 4440")
    response = await async_client.patch(
        "/users/profile",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            **data,
            "email": "another_test@test.com",
        },
    )
    assert response.status_code == 400, response.text

    response = await async_client.patch(
        "/users/profile",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            **data,
            "phone": "+1 800 444 4440",
        },
    )
    assert response.status_code == 400, response.text


@pytest.mark.asyncio
async def test_delete_profile(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")
    await delete_profile(
        async_client,
        "test@test.com",
        "password",
    )


@pytest.mark.asyncio
async def test_delete_profile_4xx(async_client):
    await signup_user(async_client, "test@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "test@test.com")

    response = await async_client.delete("/users/profile")
    assert response.status_code == 403, response.text

    response = await async_client.delete(
        "/users/profile", headers={"Authorization": "Bearer {}".format("invalid_access_token")}
    )
    assert response.status_code == 401, response.text
