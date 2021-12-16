from typing import List

from domain.models.invoices import Invoice

from .generic import AbstractFakeRepository


class InvoicesFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[Invoice]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Invoice]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Invoice:
        return await super().get(**kwargs)

    async def add(self, obj: Invoice) -> None:
        return await super().add(obj)
