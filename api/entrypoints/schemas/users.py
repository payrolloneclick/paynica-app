from typing import Optional

from pydantic import BaseModel, validator

from .validations import validate_email, validate_phone


class UserCreateRequest(BaseModel):
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


class UserUpdateRequest(BaseModel):
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


class UserPasswordRequest(BaseModel):
    password: str
    repeat_password: str

    @validator("password")
    def passwords_match(cls, v, values, **kwargs):
        if "repeat_password" in values and v != values["repeat_password"]:
            raise ValueError("Passwords do not match")
        return v


class UserEmailRequest(BaseModel):
    email: str

    @validator("email")
    def email_validator(cls, v):
        return validate_email(v)


class UserEmailCodeRequest(BaseModel):
    email_code: str


class UserPhoneRequest(BaseModel):
    phone: str

    @validator("phone")
    def phone_validator(cls, v):
        return validate_phone(v)


class UserPhoneCodeRequest(BaseModel):
    phone_code: str


class UserPresetPasswordRequest(UserPasswordRequest):
    password_code: str


class UserResponse(BaseModel):
    email: str
    phone: str
    first_name: str
    last_name: str
