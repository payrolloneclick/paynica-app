import pytest
from httpx import AsyncClient

from main import app, bus, shutdown, startup


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        await startup()
        await bus.clean()  # clean test every run
        yield client
        await shutdown()
