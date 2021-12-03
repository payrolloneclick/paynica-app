from decimal import Decimal
from typing import Optional

from pydantic.types import UUID4

from ..models.operations import Country, Currency
from .generic import AbstractReponse


class AccountResponse(AbstractReponse):
    currency: Currency
    country_alpha3: Country


class OperationResponse(AbstractReponse):
    pk: Optional[UUID4]

    sender_account: Optional[AccountResponse]
    sender_amount: Optional[Decimal]
    sender_currency: Optional[Currency]
    sender_country_alpha3: Optional[Country]

    recipient_account: Optional[AccountResponse]
    recipient_amount: Optional[Decimal]
    recipient_currency: Optional[Currency]
    recipient_country_alpha3: Optional[Country]

    punica_fee: Optional[Decimal]
    crypto_fee: Optional[Decimal]
    crypto_to_cash_fee: Optional[Decimal]