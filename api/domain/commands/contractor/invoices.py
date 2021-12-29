from decimal import Decimal
from typing import List, Optional

from pydantic.types import constr

from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class ContractorInvoiceListCommand(AbstractListCommand):
    pass


class InvoiceItemCreate(AbstractCommand):
    price: Decimal
    quantity: int
    descripion: constr(strip_whitespace=True)


class InvoiceItemUpdate(AbstractCommand):
    invoice_item_id: TPrimaryKey
    price: Optional[Decimal]
    quantity: Optional[int]
    descripion: Optional[constr(strip_whitespace=True)]


class ContractorInvoiceCreateCommand(AbstractCommand):
    for_company_id: TPrimaryKey
    recipient_account_id: TPrimaryKey
    items: List[InvoiceItemCreate]


class ContractorInvoiceRetrieveCommand(AbstractCommand):
    invoice_id: TPrimaryKey


class ContractorInvoiceUpdateCommand(AbstractCommand):
    invoice_id: TPrimaryKey
    recipient_account_id: Optional[TPrimaryKey]
    items: List[InvoiceItemUpdate]


class ContractorInvoiceDeleteCommand(AbstractCommand):
    invoice_id: TPrimaryKey
