import hashlib
import hmac
import os
import secrets
import string
from datetime import datetime
from typing import Optional

from .generic import AbstractModel


class User(AbstractModel):
    email: str
    phone: str

    first_name: str
    last_name: str
    password: Optional[str]  # we store hash of password
    last_login: Optional[datetime]

    phone_code: Optional[str]
    email_code: Optional[str]
    password_code: Optional[str]

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
