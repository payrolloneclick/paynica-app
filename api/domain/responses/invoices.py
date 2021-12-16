from decimal import Decimal
from typing import List

from pydantic.types import constr

from ..types import TPrimaryKey
from .generic import AbstractReponse


class InvoiceItem(AbstractReponse):
    pk: TPrimaryKey
    price: Decimal
    quantity: int
    descripion: constr(strip_whitespace=True)


class InvoiceResponse(AbstractReponse):
    invoice_owner_company_pk: TPrimaryKey
    invoice_owner_user_pk: TPrimaryKey
    recipient_account_pk: TPrimaryKey
    recipient_amount: Decimal
    items: List[InvoiceItem]
