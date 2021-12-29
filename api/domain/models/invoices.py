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
    created_by_id: TPrimaryKey
    created_by: Optional[User]

    for_company_id: TPrimaryKey
    for_company: Optional[Company]

    # user bank account
    recipient_account_id: TPrimaryKey
    recipient_account: Optional[RecipientBankAccount]

    # company bank account
    sender_account_id: Optional[TPrimaryKey]
    sender_account: Optional[SenderBankAccount]

    operation_id: Optional[TPrimaryKey]
    operation: Optional[Operation]


class InvoiceItem(AbstractModel):
    invoice_id: TPrimaryKey
    invoice: Optional[Invoice]
    amount: Decimal
    quantity: int
    descripion: constr(strip_whitespace=True)
