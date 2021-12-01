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


class SenderProfile(AbstractModel):
    user: User
    currency: Currency
    country_alpha3: Country


class RecipientProfile(AbstractModel):
    user: User
    currency: Currency
    country_alpha3: Country


class Operation(AbstractModel):
    sender_profile: Optional[SenderProfile] = None
    recipient_profile: Optional[RecipientProfile] = None
    sender_amount: Optional[Decimal] = None
    recipient_amount: Optional[Decimal] = None
    punica_fee: Optional[Decimal] = None
    crypto_fee: Optional[Decimal] = None
    crypto_to_cash_fee: Optional[Decimal] = None
