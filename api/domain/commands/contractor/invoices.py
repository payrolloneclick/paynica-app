from decimal import Decimal
from typing import List, Optional

from pydantic.types import constr

from domain.types import TPrimaryKey

from ..generic import AbstractCommand


class ContractorInvoiceListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class InvoiceItemCreate(AbstractCommand):
    price: Decimal
    quantity: int
    descripion: constr(strip_whitespace=True)


class InvoiceItemUpdate(AbstractCommand):
    invoice_item_pk: TPrimaryKey
    price: Optional[Decimal]
    quantity: Optional[int]
    descripion: Optional[constr(strip_whitespace=True)]


class ContractorInvoiceCreateCommand(AbstractCommand):
    recipient_account_pk: TPrimaryKey
    items: List[InvoiceItemCreate]


class ContractorInvoiceRetrieveCommand(AbstractCommand):
    invoice_pk: TPrimaryKey


class ContractorInvoiceUpdateCommand(AbstractCommand):
    invoice_pk: TPrimaryKey
    recipient_account_pk: Optional[TPrimaryKey]
    items: List[InvoiceItemUpdate]


class ContractorInvoiceDeleteCommand(AbstractCommand):
    invoice_pk: TPrimaryKey
