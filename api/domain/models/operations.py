from decimal import Decimal
from enum import Enum
from typing import Optional

from .generic import AbstractModel
from .users import User


class Currency(str, Enum):
    USD = "USD"
    GBR = "GBP"
    EUR = "EUR"
    RUB = "RUB"


class Country(str, Enum):
    USA = "USA"
    GBR = "GBR"
    RUS = "RUS"


class Account(AbstractModel):
    user: User

    currency: Currency
    country_alpha3: Country


class Operation(AbstractModel):
    user: User

    sender_account: Optional[Account]
    sender_amount: Optional[Decimal]
    sender_currency: Optional[Currency]
    sender_country_alpha3: Optional[Country]

    recipient_account: Optional[Account]
    recipient_amount: Optional[Decimal]
    recipient_currency: Optional[Currency]
    recipient_country_alpha3: Optional[Country]

    punica_fee: Optional[Decimal]
    crypto_fee: Optional[Decimal]
    crypto_to_cash_fee: Optional[Decimal]
