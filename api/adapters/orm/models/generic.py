from tortoise import fields
from tortoise.models import Model


class AbstractModel(Model):
    pk = fields.UUIDField(pk=True)

    created_date = fields.DatetimeField()
    updated_date = fields.DatetimeField()

    class Meta:
        abstract = True
