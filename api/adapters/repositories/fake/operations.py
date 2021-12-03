from typing import List

from domain.models.operations import Account, Operation

from .generic import AbstractFakeRepository


class AccountFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[Account]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Account]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Account:
        return await super().get(**kwargs)

    async def add(self, obj: Account) -> None:
        return await super().add(obj)


class OperationsFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[Operation]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Operation]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Operation:
        return await super().get(**kwargs)

    async def add(self, obj: Operation) -> None:
        return await super().add(obj)
