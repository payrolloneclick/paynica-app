from typing import Optional

from httpx import AsyncClient

from domain.types import TPrimaryKey

from ..users import signin_generate_access_token


async def list_companies(
    async_client: AsyncClient,
    email: str,
    password: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> dict:
    response = await signin_generate_access_token(async_client, email, password)
    access_token = response["access_token"]
    url = f"/contractor/companies?limit={limit}&offset={offset}"
    if search:
        url += f"&search={search}"
    if sort_by:
        url += f"&sort_by={search}"
    response = await async_client.get(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 200, response.text
    companies = response.json()
    if companies:
        company = companies[0]
        assert "id" in company
    return companies


async def retrieve_company(
    async_client: AsyncClient,
    email: str,
    password: str,
    id: TPrimaryKey,
) -> dict:
    response = await signin_generate_access_token(async_client, email, password)
    access_token = response["access_token"]
    url = f"/contractor/companies/{id}"
    response = await async_client.get(
        url,
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 200, response.text
    company = response.json()
    assert "id" in company
    return company


async def leave_company(
    async_client: AsyncClient,
    email: str,
    password: str,
    id: TPrimaryKey,
) -> dict:
    response = await signin_generate_access_token(async_client, email, password)
    access_token = response["access_token"]
    url = f"/contractor/companies/{id}/leave"
    response = await async_client.post(url, headers={"Authorization": "Bearer {}".format(access_token)}, json={})
    assert response.status_code == 200, response.text
    assert response.json() is None
