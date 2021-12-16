from decimal import Decimal
from typing import Optional

from pydantic.types import constr

from ..types import TPrimaryKey
from .bank_accounts import RecipientBankAccount
from .companies import Company
from .generic import AbstractModel
from .users import User


class Invoice(AbstractModel):
    invoice_owner_company_pk: TPrimaryKey
    invoice_owner_company: Optional[Company]
    invoice_owner_user_pk: TPrimaryKey
    invoice_owner_user: Optional[User]
    recipient_account_pk: TPrimaryKey
    recipient_account: Optional[RecipientBankAccount]
    recipient_amount: Decimal


class InvoiceItem(AbstractModel):
    invoice_pk: TPrimaryKey
    invoice: Optional[Invoice]
    price: Decimal
    quantity: int
    descripion: constr(strip_whitespace=True)
