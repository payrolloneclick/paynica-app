from typing import Optional

from pydantic import validator
from pydantic.types import UUID4

from domain.models.users import User

from ..validations import validate_email, validate_phone
from .generic import AbstractCommand


class CreateUserCommand(AbstractCommand):
    email: str
    phone: str
    first_name: str
    last_name: str
    password: str
    repeat_password: str

    @validator("password")
    def passwords_match(cls, v, values, **kwargs):
        if "repeat_password" in values and v != values["repeat_password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("email")
    def email_validator(cls, v):
        return validate_email(v)

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class RetrieveUserCommand(AbstractCommand):
    pk: UUID4


class UpdateUserCommand(AbstractCommand):
    email: Optional[str]
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    repeat_password: Optional[str]

    @validator("password")
    def passwords_match(cls, v, values, **kwargs):
        if "repeat_password" in values and v != values["repeat_password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("email")
    def email_validator(cls, v):
        return validate_email(v)

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class DeleteUserCommand(AbstractCommand):
    pk: UUID4


class UserChangePasswordCommand(AbstractCommand):
    password: str
    repeat_password: str

    @validator("password")
    def passwords_match(cls, v, values, **kwargs):
        if "repeat_password" in values and v != values["repeat_password"]:
            raise ValueError("Passwords do not match")
        return v


class GenerateEmailCodeCommand(AbstractCommand):
    email: str

    @validator("email")
    def email_validator(cls, v):
        return validate_email(v)


class SendEmailCodeByEmailCommand(AbstractCommand):
    user: User


class VerifyEmailCodeCommand(AbstractCommand):
    email_code: str


class GeneratePhoneCodeCommand(AbstractCommand):
    phone: str

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class SendPhoneCodeBySmsCommand(AbstractCommand):
    user: User


class VerifyPhoneCodeCommand(AbstractCommand):
    phone_code: str


class GenerateResetPasswordCodeCommand(GenerateEmailCodeCommand):
    pass


class SendResetPasswordCodeByEmailCommand(SendEmailCodeByEmailCommand):
    pass


class ResetPasswordCommand(UserChangePasswordCommand):
    password_code: str
