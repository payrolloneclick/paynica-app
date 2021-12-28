import pytest

from domain.types import TRole

from .scenarios.contractor.companies import list_companies
from .scenarios.employer.companies import create_company
from .scenarios.users import invite_user, signup_user, signup_verify_email


@pytest.mark.asyncio
async def test_companies_list(async_client):
    await signup_user(async_client, "employer@test.com", TRole.EMPLOYER, "password")
    await signup_verify_email(async_client, "employer@test.com")
    await signup_user(async_client, "contractor@test.com", TRole.CONTRACTOR, "password")
    await signup_verify_email(async_client, "contractor@test.com")
    for i in range(2):
        company = await create_company(async_client, "employer@test.com", "password", f"Employer Company {i}")
        await invite_user(async_client, company["pk"], "employer@test.com", "password", "contractor@test.com")

    company_data = await list_companies(
        async_client,
        "contractor@test.com",
        "password",
        2,
        limit=10,
        offset=0,
    )
    assert len(company_data) == 2

    company_data = await list_companies(
        async_client,
        "contractor@test.com",
        "password",
        2,
        limit=1,
        offset=0,
    )
    assert len(company_data) == 1

    company_data = await list_companies(
        async_client,
        "contractor@test.com",
        "password",
        2,
        limit=1,
        offset=2,
    )
    assert len(company_data) == 0
