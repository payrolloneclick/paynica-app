import hashlib
import hmac
import os
import secrets
import string
from datetime import datetime
from typing import Optional

from pydantic.types import constr

from ..validations import EMAIL_REGEXP
from .generic import AbstractModel


class User(AbstractModel):
    email: constr(strip_whitespace=True, to_lower=True, regex=EMAIL_REGEXP)
    phone: constr(strip_whitespace=True, to_lower=True)

    first_name: constr(strip_whitespace=True)
    last_name: constr(strip_whitespace=True)
    password: Optional[constr(strip_whitespace=True)]  # we store hash of password
    last_login: Optional[datetime]

    phone_code: Optional[constr(strip_whitespace=True, min_length=6)]
    email_code: Optional[constr(strip_whitespace=True, min_length=16)]
    password_code: Optional[constr(strip_whitespace=True, min_length=16)]

    is_phone_verified: Optional[bool] = False
    is_email_verified: Optional[bool] = False
    is_active: Optional[bool] = False

    async def _get_password_hash(self, password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)

    async def set_password(self, password: str) -> None:
        salt = os.urandom(16)
        password_hash = await self._get_password_hash(password, salt)
        self.password = f"{salt.hex()}${password_hash.hex()}"

    async def verify_password(self, password: str) -> bool:
        if not self.password:
            return False
        salt, db_password_hash = self.password.split("$")
        password_hash = await self._get_password_hash(password, bytes.fromhex(salt))
        password_hash = password_hash.hex()
        return hmac.compare_digest(db_password_hash, password_hash)

    async def randomly_set_phone_code(self, length: int = 6) -> None:
        self.phone_code = "".join(secrets.choice(string.digits) for _ in range(length))

    async def randomly_set_email_code(self, length: int = 16) -> None:
        self.email_code = secrets.token_hex(length)

    async def randomly_set_password_code(self, length: int = 16) -> None:
        self.password_code = secrets.token_hex(length)
