from tortoise import fields

from domain.models.users import User
from domain.types import TRole

from .generic import ORMAbstractModel


class ChoiceField(fields.CharField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices", [])
        super().__init__(*args, **kwargs)

    def to_db_value(self, value: any, instance: any) -> any:
        value = super().to_db_value(value, instance)
        return value._value_


class ORMUser(ORMAbstractModel):
    email = fields.CharField(max_length=255)
    role = ChoiceField(max_length=16, choices=TRole)

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

    class Meta:
        pydantic_cls = User
