from typing import Optional

from ..types import TCountry, TCurrency, TPrimaryKey
from .generic import AbstractReponse


class SenderBankAccountResponse(AbstractReponse):
    sender_owner_company_pk: Optional[TPrimaryKey]
    sender_owner_user_pk: Optional[TPrimaryKey]

    sender_currency: TCurrency
    sender_country_alpha3: TCountry


class RecipientBankAccountResponse(AbstractReponse):
    recipient_owner_company_pk: Optional[TPrimaryKey]
    recipient_owner_user_pk: Optional[TPrimaryKey]

    recipient_currency: TCurrency
    recipient_country_alpha3: TCountry
