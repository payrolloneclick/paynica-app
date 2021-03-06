from decimal import Decimal
from typing import List

from pydantic.types import constr

from ..types import TPrimaryKey
from .generic import AbstractReponse


class InvoiceItem(AbstractReponse):
    id: TPrimaryKey
    price: Decimal
    quantity: int
    descripion: constr(strip_whitespace=True)


class InvoiceResponse(AbstractReponse):
    id: TPrimaryKey
    invoice_owner_company_id: TPrimaryKey
    invoice_owner_user_id: TPrimaryKey
    recipient_account_id: TPrimaryKey
    recipient_amount: Decimal
    items: List[InvoiceItem]
