import uuid

import pytest

from bootstrap import bus
from domain.types import TRole

from .scenarios.employer.companies import create_company
from .scenarios.users import signin_generate_access_token, signup_user, signup_verify_email


@pytest.mark.asyncio
async def test_create_company(async_client):
    db_user = await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    company_data = await create_company(async_client, "employer@test.com", "password", "Employer Company")
    company_pk = company_data["pk"]
    async with bus.uow:
        assert await bus.uow.companies_m2m_employers.exists(company_pk=uuid.UUID(company_pk), employer_pk=db_user.pk)
        assert not await bus.uow.companies_m2m_contractors.exists(
            company_pk=uuid.UUID(company_pk), contractor_pk=db_user.pk
        )


@pytest.mark.asyncio
async def test_create_company_4xx(async_client):
    create_company_url = "/employer/companies"
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")

    response = await async_client.post(
        create_company_url,
        json={
            "name": "Employer Company",
        },
    )
    assert response.status_code == 403, response.text

    response = await signin_generate_access_token(async_client, "employer@test.com", "password")
    access_token = response["access_token"]

    response = await async_client.post(
        create_company_url,
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={},
    )
    assert response.status_code == 422, response.text

    response = await async_client.post(
        create_company_url,
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            "name": "",
        },
    )
    assert response.status_code == 400, response.text

    response = await async_client.post(
        create_company_url,
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            "name": "Employer Company",
        },
    )
    assert response.status_code == 200, response.text

    response = await async_client.post(
        create_company_url,
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            "name": "Employer Company",
        },
    )
    # same name for this user
    assert response.status_code == 400, response.text

    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")

    response = await signin_generate_access_token(async_client, "contractor@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.post(
        create_company_url,
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            "name": "Employer Company",
        },
    )
    assert response.status_code == 403, response.text
