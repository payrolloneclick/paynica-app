from decimal import Decimal
from typing import Optional

from pydantic.types import constr

from ..types import TPrimaryKey
from .bank_accounts import RecipientBankAccount, SenderBankAccount
from .companies import Company
from .generic import AbstractModel
from .operations import Operation
from .users import User


class Invoice(AbstractModel):
    created_by_pk: TPrimaryKey
    created_by: Optional[User]

    # user bank account
    recipient_account_pk: TPrimaryKey
    recipient_account: Optional[RecipientBankAccount]

    for_company_pk: TPrimaryKey
    for_company: Optional[Company]

    # company bank account
    sender_account_pk: Optional[TPrimaryKey]
    sender_account: Optional[SenderBankAccount]

    operation_pk: Optional[TPrimaryKey]
    operation: Optional[Operation]


class InvoiceItem(AbstractModel):
    invoice_pk: TPrimaryKey
    invoice: Optional[Invoice]
    amount: Decimal
    quantity: int
    descripion: constr(strip_whitespace=True)
