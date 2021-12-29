from typing import List, Optional

from adapters.orm.models.bank_accounts import ORMRecipientBankAccount, ORMSenderBankAccount
from domain.models.bank_accounts import RecipientBankAccount, SenderBankAccount

from .generic import AbstractDBRepository


class SenderBankAccountDBRepository(AbstractDBRepository):
    orm_model_cls: type[ORMSenderBankAccount] = ORMSenderBankAccount

    async def all(self) -> List[SenderBankAccount]:
        return await super().all()

    async def filter(self, **kwargs) -> List[SenderBankAccount]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> SenderBankAccount:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[SenderBankAccount]:
        return await super().first(**kwargs)

    async def add(self, obj: SenderBankAccount) -> None:
        return await super().add(obj)


class RecipientBankAccountDBRepository(AbstractDBRepository):
    orm_model_cls: type[ORMRecipientBankAccount] = ORMRecipientBankAccount

    async def all(self) -> List[RecipientBankAccount]:
        return await super().all()

    async def filter(self, **kwargs) -> List[RecipientBankAccount]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> RecipientBankAccount:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[RecipientBankAccount]:
        return await super().first(**kwargs)

    async def add(self, obj: RecipientBankAccount) -> None:
        return await super().add(obj)
