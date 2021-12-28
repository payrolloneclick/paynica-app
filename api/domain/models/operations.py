from decimal import Decimal
from typing import Optional

from ..types import TOperationStatus, TPrimaryKey
from .bank_accounts import RecipientBankAccount, SenderBankAccount
from .companies import Company
from .generic import AbstractModel
from .users import User


class Operation(SenderBankAccount, RecipientBankAccount, AbstractModel):
    operation_owner_company_pk: TPrimaryKey
    operation_owner_company: Optional[Company]

    operation_sender_user_pk: TPrimaryKey
    operation_sender_user: Optional[User]
    operation_recipient_user_pk: TPrimaryKey
    operation_recipient_user: Optional[User]

    sender_account_pk: Optional[TPrimaryKey]
    sender_account: Optional[SenderBankAccount]
    sender_amount: Optional[Decimal]

    recipient_account_pk: Optional[TPrimaryKey]
    recipient_account: Optional[RecipientBankAccount]
    recipient_amount: Optional[Decimal]

    status: TOperationStatus
    our_fee: Optional[Decimal]
    provider_fee: Optional[Decimal]
