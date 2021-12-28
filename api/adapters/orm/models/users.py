from tortoise import fields

from .generic import AbstractModel


class User(AbstractModel):
    email = fields.CharField(max_length=255)
    role = fields.CharField(max_length=16)

    phone = fields.CharField(max_length=255, null=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255, null=True)
    last_login = fields.DatetimeField(null=True)

    phone_code = fields.CharField(max_length=8, null=True)
    email_code = fields.CharField(max_length=255, null=True)
    password_code = fields.CharField(max_length=255, null=True)

    is_phone_verified = fields.BooleanField(default=False)
    is_email_verified = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)
    is_onboarded = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
