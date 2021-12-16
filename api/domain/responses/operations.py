from decimal import Decimal
from typing import Optional

from pydantic.types import UUID4

from ..types import TCountry, TCurrency
from .generic import AbstractReponse


class AccountResponse(AbstractReponse):
    currency: TCurrency
    country_alpha3: TCountry


class OperationResponse(AbstractReponse):
    pk: Optional[UUID4]

    sender_account: Optional[AccountResponse]
    sender_amount: Optional[Decimal]
    sender_currency: Optional[TCurrency]
    sender_country_alpha3: Optional[TCountry]

    recipient_account: Optional[AccountResponse]
    recipient_amount: Optional[Decimal]
    recipient_currency: Optional[TCurrency]
    recipient_country_alpha3: Optional[TCountry]

    punica_fee: Optional[Decimal]
    crypto_fee: Optional[Decimal]
    crypto_to_cash_fee: Optional[Decimal]
