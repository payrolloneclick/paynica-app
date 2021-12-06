from typing import Optional

from pydantic import validator
from pydantic.types import UUID4, constr

from domain.models.users import User

from ..validations import EMAIL_REGEXP, validate_phone
from .generic import AbstractCommand


class GenerateAccessTokenCommand(AbstractCommand):
    email: constr(strip_whitespace=True, to_lower=True, regex=EMAIL_REGEXP)
    password: constr(strip_whitespace=True, min_length=8)


class RefreshAccessTokenCommand(AbstractCommand):
    refresh_token: constr(strip_whitespace=True, min_length=1)


class CreateUserCommand(AbstractCommand):
    email: constr(strip_whitespace=True, to_lower=True, regex=EMAIL_REGEXP)
    phone: constr(strip_whitespace=True, to_lower=True, min_length=1)
    first_name: constr(strip_whitespace=True)
    last_name: constr(strip_whitespace=True)
    password: constr(strip_whitespace=True, min_length=8)
    repeat_password: constr(strip_whitespace=True, min_length=8)

    @validator("repeat_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class RetrieveUserCommand(AbstractCommand):
    pk: UUID4


class UpdateUserCommand(AbstractCommand):
    email: Optional[constr(strip_whitespace=True, to_lower=True, regex=EMAIL_REGEXP)]
    phone: Optional[constr(strip_whitespace=True, to_lower=True, min_length=1)]
    first_name: Optional[constr(strip_whitespace=True)]
    last_name: Optional[constr(strip_whitespace=True)]
    password: Optional[constr(strip_whitespace=True, min_length=8)]
    repeat_password: Optional[constr(strip_whitespace=True, min_length=8)]

    @validator("repeat_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class DeleteUserCommand(AbstractCommand):
    pk: UUID4


class UserChangePasswordCommand(AbstractCommand):
    password: constr(strip_whitespace=True, min_length=8)
    repeat_password: constr(strip_whitespace=True, min_length=8)

    @validator("repeat_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class GenerateEmailCodeCommand(AbstractCommand):
    email: constr(strip_whitespace=True, to_lower=True, regex=EMAIL_REGEXP)


class SendEmailCodeByEmailCommand(AbstractCommand):
    user: User


class VerifyEmailCodeCommand(AbstractCommand):
    email_code: constr(strip_whitespace=True, min_length=16)


class GeneratePhoneCodeCommand(AbstractCommand):
    phone: constr(strip_whitespace=True, to_lower=True, min_length=1)

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class SendPhoneCodeBySmsCommand(AbstractCommand):
    user: User


class VerifyPhoneCodeCommand(AbstractCommand):
    phone_code: constr(strip_whitespace=True, min_length=6)


class GenerateResetPasswordCodeCommand(GenerateEmailCodeCommand):
    pass


class SendResetPasswordCodeByEmailCommand(SendEmailCodeByEmailCommand):
    pass


class ResetPasswordCommand(UserChangePasswordCommand):
    password_code: constr(strip_whitespace=True, min_length=16)
