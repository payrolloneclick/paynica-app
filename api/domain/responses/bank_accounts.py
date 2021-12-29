from typing import Optional

from ..types import TBankAccountType, TCountry, TCurrency, TPrimaryKey
from .generic import AbstractReponse


class SenderBankAccountResponse(AbstractReponse):
    id: TPrimaryKey
    sender_owner_company_id: Optional[TPrimaryKey]
    sender_owner_user_id: Optional[TPrimaryKey]

    sender_bank_account_type: TBankAccountType
    sender_currency: TCurrency
    sender_country_alpha3: TCountry


class RecipientBankAccountResponse(AbstractReponse):
    id: TPrimaryKey
    recipient_owner_company_id: Optional[TPrimaryKey]
    recipient_owner_user_id: Optional[TPrimaryKey]

    recipient_bank_account_type: TBankAccountType
    recipient_currency: TCurrency
    recipient_country_alpha3: TCountry
