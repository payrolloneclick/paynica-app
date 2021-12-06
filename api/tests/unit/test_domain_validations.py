import pytest

from domain.validations import validate_phone


@pytest.mark.asyncio
async def test_validate_phone():
    assert validate_phone(None) is None
    assert validate_phone("") == ""
    with pytest.raises(ValueError):
        assert validate_phone("invalid")
