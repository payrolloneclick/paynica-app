from typing import Optional

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    email: str
    phone: str
    first_name: str
    last_name: str
    password: str
    repeat_password: str


class UserUpdateRequest(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    repeat_password: Optional[str]


class UserPasswordRequest(BaseModel):
    password: str
    repeat_password: str


class UserEmailRequest(BaseModel):
    email: str


class UserEmailCodeRequest(BaseModel):
    email_code: str


class UserPhoneRequest(BaseModel):
    email: str


class UserPhoneCodeRequest(BaseModel):
    email_code: str


class UserPresetPasswordRequest(UserPasswordRequest):
    password_code: str


class UserResponse(BaseModel):
    email: str
    phone: str
    first_name: str
    last_name: str
