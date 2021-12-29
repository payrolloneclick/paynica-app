from typing import List, Optional

from adapters.orm.models.invoices import ORMInvoice, ORMInvoiceItem
from domain.models.invoices import Invoice, InvoiceItem
from settings import DEFAULT_LIMIT

from .generic import AbstractDBRepository


class InvoicesDBRepository(AbstractDBRepository):
    orm_model_cls: type[ORMInvoice] = ORMInvoice

    async def list(
        self,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        **kwargs,
    ) -> List[Invoice]:
        return await super().list(search=search, sort_by=sort_by, offset=offset, limit=limit, **kwargs)

    async def all(self) -> List[Invoice]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Invoice]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Invoice:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[Invoice]:
        return await super().first(**kwargs)

    async def add(self, obj: Invoice) -> None:
        return await super().add(obj)


class InvoiceItemsDBRepository(AbstractDBRepository):
    orm_model_cls: type[ORMInvoiceItem] = ORMInvoiceItem

    async def list(
        self,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        **kwargs,
    ) -> List[InvoiceItem]:
        return await super().list(search=search, sort_by=sort_by, offset=offset, limit=limit, **kwargs)

    async def all(self) -> List[InvoiceItem]:
        return await super().all()

    async def filter(self, **kwargs) -> List[InvoiceItem]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> InvoiceItem:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[InvoiceItem]:
        return await super().first(**kwargs)

    async def add(self, obj: InvoiceItem) -> None:
        return await super().add(obj)
