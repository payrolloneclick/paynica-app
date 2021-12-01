from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    email: str
    phone: str
    first_name: str
    last_name: str
    password: str
    repeat_password: str


class UserPasswordrequest(BaseModel):
    password: str
    repeat_password: str


class UserResponse(BaseModel):
    email: str
    phone: str
    first_name: str
    last_name: str
