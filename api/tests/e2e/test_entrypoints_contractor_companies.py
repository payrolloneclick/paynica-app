from uuid import uuid4

import pytest

from domain.types import TRole

from .scenarios.contractor.companies import leave_company, list_companies, retrieve_company
from .scenarios.employer.companies import create_company
from .scenarios.users import invite_user, signin_generate_access_token, signup_user, signup_verify_email


@pytest.mark.asyncio
async def test_companies_list(async_client):
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")
    await create_company(async_client, "employer@test.com", "password", "Employer Company")
    for i in range(2):
        company = await create_company(async_client, "employer@test.com", "password", f"Employer Company {i}")
        await invite_user(async_client, company["id"], "employer@test.com", "password", "contractor@test.com")

    company_data = await list_companies(
        async_client,
        "contractor@test.com",
        "password",
        limit=10,
        offset=0,
    )
    assert len(company_data) == 2

    company_data = await list_companies(
        async_client,
        "contractor@test.com",
        "password",
        limit=1,
        offset=0,
    )
    assert len(company_data) == 1

    company_data = await list_companies(
        async_client,
        "contractor@test.com",
        "password",
        limit=1,
        offset=2,
    )
    assert len(company_data) == 0


@pytest.mark.asyncio
async def test_companies_list_4xx(async_client):
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")

    url = "/contractor/companies"
    response = await async_client.get(url)
    assert response.status_code == 403, response.text

    response = await signin_generate_access_token(async_client, "employer@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.get(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_companies_retrieve(async_client):
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")

    company = await create_company(async_client, "employer@test.com", "password", "Employer Company")
    await invite_user(async_client, company["id"], "employer@test.com", "password", "contractor@test.com")

    company_data = await retrieve_company(
        async_client,
        "contractor@test.com",
        "password",
        company["id"],
    )
    assert company_data["id"] == company["id"]


@pytest.mark.asyncio
async def test_companies_retrieve_4xx(async_client):
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")

    company = await create_company(async_client, "employer@test.com", "password", "Employer Company")
    id = company["id"]

    url = f"/contractor/companies/{id}"

    response = await async_client.get(url)
    assert response.status_code == 403, response.text

    response = await signin_generate_access_token(async_client, "contractor@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.get(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text

    await invite_user(async_client, id, "employer@test.com", "password", "contractor@test.com")
    response = await async_client.get(
        f"/contractor/companies/{uuid4()}",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text

    response = await signin_generate_access_token(async_client, "employer@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.get(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_companies_leave(async_client):
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")

    company = await create_company(async_client, "employer@test.com", "password", "Employer Company")
    id = company["id"]
    await invite_user(async_client, id, "employer@test.com", "password", "contractor@test.com")

    response = await signin_generate_access_token(async_client, "contractor@test.com", "password")
    access_token = response["access_token"]

    url = f"/contractor/companies/{id}"
    response = await async_client.get(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 200, response.text

    await leave_company(
        async_client,
        "contractor@test.com",
        "password",
        id,
    )
    response = await async_client.get(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_companies_leave_4xx(async_client):
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")

    company = await create_company(async_client, "employer@test.com", "password", "Employer Company")
    id = company["id"]

    url = f"/contractor/companies/{id}/leave"

    response = await async_client.post(url)
    assert response.status_code == 403, response.text

    response = await signin_generate_access_token(async_client, "contractor@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.post(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text

    await invite_user(async_client, id, "employer@test.com", "password", "contractor@test.com")
    response = await async_client.post(
        f"/contractor/companies/{uuid4()}/leave",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text

    response = await signin_generate_access_token(async_client, "employer@test.com", "password")
    access_token = response["access_token"]
    response = await async_client.post(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 403, response.text
