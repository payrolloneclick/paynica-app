import uuid

import pytest

from domain.models.users import User
from domain.types import TRole


@pytest.mark.asyncio
async def test_verify_password():
    user = User(
        id=uuid.uuid4(),
        role=TRole.EMPLOYER,
        email="test@test.com",
        phone="+1 800 444 4444",
        first_name="first name",
        last_name="last name",
    )
    assert not user.password
    assert not await user.verify_password("password")
    await user.set_password("password")
    assert await user.verify_password("password")
