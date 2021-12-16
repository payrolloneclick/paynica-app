from typing import Optional

from pydantic import validator
from pydantic.types import constr

from domain.models.users import User

from ..types import (
    TEmail,
    TEmailCode,
    TInvitationCode,
    TPassword,
    TPasswordCode,
    TPhone,
    TPhoneCode,
    TPrimaryKey,
    TRole,
)
from ..validations import validate_phone
from .generic import AbstractCommand


class GenerateAccessTokenCommand(AbstractCommand):
    email: TEmail
    password: TPassword


class RefreshAccessTokenCommand(AbstractCommand):
    refresh_token: constr(strip_whitespace=True, min_length=1)


class SignUpUserCommand(AbstractCommand):
    email: TEmail
    role: TRole
    password: TPassword
    repeat_password: TPassword
    invitation_code: Optional[TInvitationCode]

    @validator("repeat_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class GenerateEmailCodeCommand(AbstractCommand):
    email: TEmail


class SendEmailCodeByEmailCommand(AbstractCommand):
    user: User


class VerifyEmailCodeCommand(AbstractCommand):
    email_code: TEmailCode


class GeneratePhoneCodeCommand(AbstractCommand):
    phone: TPhone

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class SendPhoneCodeBySmsCommand(AbstractCommand):
    user: User


class VerifyPhoneCodeCommand(AbstractCommand):
    phone_code: TPhoneCode


class GenerateResetPasswordCodeCommand(GenerateEmailCodeCommand):
    pass


class SendResetPasswordCodeByEmailCommand(SendEmailCodeByEmailCommand):
    pass


class ResetPasswordCommand(AbstractCommand):
    password: TPassword
    repeat_password: TPassword
    password_code: TPasswordCode

    @validator("repeat_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class ProfileRetrieveCommand(AbstractCommand):
    pass


class ProfileUpdateCommand(AbstractCommand):
    email: Optional[TEmail]
    phone: Optional[TPhone]
    first_name: Optional[constr(strip_whitespace=True)]
    last_name: Optional[constr(strip_whitespace=True)]

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class ProfileDeleteCommand(AbstractCommand):
    pass


class ChangePasswordCommand(AbstractCommand):
    password: TPassword
    repeat_password: TPassword

    @validator("repeat_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class GenerateInvitationCodeCommand(AbstractCommand):
    company_pk: TPrimaryKey
    email: TEmail


class SendInvitationCodeByEmailCommand(AbstractCommand):
    company_pk: TPrimaryKey
    user: User


class VerifyInvitationCodeAndInviteUserToCompanyCommand(AbstractCommand):
    invitation_code: TInvitationCode
