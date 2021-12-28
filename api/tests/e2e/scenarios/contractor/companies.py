from typing import Optional

from httpx import AsyncClient

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
    return companies
