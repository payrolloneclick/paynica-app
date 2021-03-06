from typing import Optional

from ..types import TBankAccountType, TCountry, TCurrency, TPrimaryKey
from .companies import Company
from .generic import AbstractModel
from .users import User


class SenderBankAccount(AbstractModel):
    sender_owner_user_id: Optional[TPrimaryKey]
    sender_owner_user: Optional[User]
    sender_owner_company_id: Optional[TPrimaryKey]
    sender_owner_company: Optional[Company]

    sender_bank_account_type: TBankAccountType
    sender_currency: TCurrency
    sender_country_alpha3: TCountry


class RecipientBankAccount(AbstractModel):
    recipient_owner_user_id: Optional[TPrimaryKey]
    recipient_owner_user: Optional[User]
    recipient_owner_company_id: Optional[TPrimaryKey]
    recipient_owner_company: Optional[Company]

    recipient_bank_account_type: TBankAccountType
    recipient_currency: TCurrency
    recipient_country_alpha3: TCountry
