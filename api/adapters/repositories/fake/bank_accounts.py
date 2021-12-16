from typing import List

from domain.models.bank_accounts import RecipientBankAccount, SenderBankAccount

from .generic import AbstractFakeRepository


class SenderBankAccountFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[SenderBankAccount]:
        return await super().all()

    async def filter(self, **kwargs) -> List[SenderBankAccount]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> SenderBankAccount:
        return await super().get(**kwargs)

    async def add(self, obj: SenderBankAccount) -> None:
        return await super().add(obj)


class RecipientBankAccountFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[RecipientBankAccount]:
        return await super().all()

    async def filter(self, **kwargs) -> List[RecipientBankAccount]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> RecipientBankAccount:
        return await super().get(**kwargs)

    async def add(self, obj: RecipientBankAccount) -> None:
        return await super().add(obj)
