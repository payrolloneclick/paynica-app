from httpx import AsyncClient

from ..users import signin_generate_access_token


async def create_company(
    async_client: AsyncClient,
    email: str,
    password: str,
    company_name: str,
) -> dict:
    response = await signin_generate_access_token(async_client, email, password)
    access_token = response["access_token"]
    response = await async_client.post(
        "/employer/companies",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={
            "name": company_name,
        },
    )
    assert response.status_code == 200, response.text
    company_data = response.json()
    for field in ("id",):
        assert field in company_data, field
    return company_data
