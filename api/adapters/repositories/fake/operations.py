from typing import List

from domain.models.operations import Operation

from .generic import AbstractFakeRepository


class OperationsFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[Operation]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Operation]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Operation:
        return await super().get(**kwargs)

    async def add(self, obj: Operation) -> None:
        return await super().add(obj)
