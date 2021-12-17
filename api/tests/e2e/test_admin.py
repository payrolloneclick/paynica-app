import pytest

from bootstrap import bus
from domain.types import TRole

from .scenarios.users import signin_generate_access_token, signup_user, signup_verify_email

RESOURCES = (
    "users",
    "companies",
    "companies_m2m_contractors",
    "companies_m2m_employers",
    "invite_users_to_companies",
    "recipient_bank_accounts",
    "sender_bank_accounts",
    "invoices",
    "operations",
)


@pytest.mark.asyncio
async def test_list(async_client):
    resource_url = "/admin/resources/%s"
    db_user = await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    response = await signin_generate_access_token(async_client, "employer@test.com", "password")
    access_token = response["access_token"]

    async with bus.uow:
        db_user.is_superuser = True
        await bus.uow.users.update(db_user)

    for resource in RESOURCES:
        url = resource_url % resource
        response = await async_client.get(
            url,
            headers={"Authorization": "Bearer {}".format(access_token)},
        )
        assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_list_4xx(async_client):
    resource_url = "/admin/resources/%s"

    for resource in RESOURCES:
        url = resource_url % resource
        response = await async_client.get(
            url,
        )
        assert response.status_code == 403, response.text

    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    response = await signin_generate_access_token(async_client, "employer@test.com", "password")
    access_token = response["access_token"]

    for resource in RESOURCES:
        url = resource_url % resource
        response = await async_client.get(
            url,
            headers={"Authorization": "Bearer {}".format(access_token)},
        )
        # not admin
        assert response.status_code == 403, response.text
