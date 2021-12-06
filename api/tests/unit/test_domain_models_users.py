import uuid

import pytest

from domain.models.users import User


@pytest.mark.asyncio
async def test_verify_password():
    user = User(
        pk=uuid.uuid4(),
        email="test@test.com",
        phone="+1 800 444 4444",
        first_name="first name",
        last_name="last name",
    )
    assert not user.password
    assert not await user.verify_password("password")
    await user.set_password("password")
    assert await user.verify_password("password")
