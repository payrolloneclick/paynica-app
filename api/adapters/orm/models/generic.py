from tortoise import fields
from tortoise.models import Model

from domain.models.generic import AbstractModel


class ORMAbstractModel(Model):
    id = fields.UUIDField(pk=True)

    created_date = fields.DatetimeField()
    updated_date = fields.DatetimeField(null=True)

    def to_dict(self) -> dict:
        return {i: v for i, v in self.__dict__.items() if not i.startswith("_")}

    def from_pydantic(self, pydantic_obj: AbstractModel) -> None:
        self.update_from_dict(pydantic_obj.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True))

    def to_pydantic(self) -> AbstractModel:
        pydantic_cls: AbstractModel = getattr(self.Meta, "pydantic_cls")
        obj = pydantic_cls(**self.to_dict())
        return obj

    class Meta:
        abstract = True
        pydantic_cls = AbstractModel
