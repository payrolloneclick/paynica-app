from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    email: str
    phone: str
    first_name: str
    last_name: str
    password: str
    repeat_password: str


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
