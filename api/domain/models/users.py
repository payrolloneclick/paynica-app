import hashlib
import hmac
import os
import secrets
import string
from datetime import datetime
from typing import Optional

from pydantic.types import UUID4


class User:
    def __init__(
        self,
        pk: UUID4,
        email: str,
        phone: str,
        first_name: str,
        last_name: str,
        password_hash: Optional[str] = None,
        phone_code: Optional[str] = None,
        email_code: Optional[str] = None,
        password_code: Optional[str] = None,
        is_phone_verified: Optional[bool] = False,
        is_email_verified: Optional[bool] = False,
        is_active: Optional[bool] = False,
        last_login: Optional[datetime] = None,
        created_date: Optional[datetime] = None,
        updated_date: Optional[datetime] = None,
    ):
        self.pk = pk
        self.email = email
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.phone_code = phone_code
        self.email_code = email_code
        self.password_code = password_code
        self.is_phone_verified = is_phone_verified
        self.is_email_verified = is_email_verified
        self.is_active = is_active
        self.last_login = last_login
        self.created_date = created_date
        self.updated_date = updated_date

    async def _get_password_hash(self, password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)

    async def set_password_hash(self, password: str) -> None:
        salt = os.urandom(16)
        password_hash = await self._get_password_hash(password, salt)
        self.password_hash = f"{salt.hex()}${password_hash.hex()}"

    async def verify_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        salt, db_password_hash = self.password_hash.split("$")
        password_hash = await self._get_password_hash(password, bytes.fromhex(salt))
        password_hash = password_hash.hex()
        return hmac.compare_digest(db_password_hash, password_hash)

    async def randomly_set_phone_verification_code(self, length: int = 6) -> None:
        self.phone_code = "".join(secrets.choice(string.digits) for _ in range(length))

    async def randomly_set_email_verification_code(self, length: int = 16) -> None:
        self.email_code = secrets.token_hex(length)
