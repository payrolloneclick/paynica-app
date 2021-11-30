from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic.types import UUID4

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


class SenderProfile:
    def __init__(
        self,
        pk: UUID4,
        user: User,
        currency: Currency,
        country_alpha3: Country,
        created_date: Optional[datetime] = None,
        updated_date: Optional[datetime] = None,
    ):
        self.pk = pk
        self.user = user
        self.currency = currency
        self.country_alpha3 = country_alpha3
        self.created_date = created_date
        self.updated_date = updated_date


class RecipientProfile:
    def __init__(
        self,
        pk: UUID4,
        user: User,
        currency: Currency,
        country_alpha3: Country,
        created_date: Optional[datetime] = None,
        updated_date: Optional[datetime] = None,
    ):
        self.pk = pk
        self.user = user
        self.currency = currency
        self.country_alpha3 = country_alpha3
        self.created_date = created_date
        self.updated_date = updated_date


class Operation:
    def __init__(
        self,
        pk: UUID4,
        sender_profile: Optional[SenderProfile] = None,
        recipient_profile: Optional[RecipientProfile] = None,
        sender_amount: Optional[Decimal] = None,
        recipient_amount: Optional[Decimal] = None,
        punica_fee: Optional[Decimal] = None,
        crypto_fee: Optional[Decimal] = None,
        crypto_to_cash_fee: Optional[Decimal] = None,
        created_date: Optional[datetime] = None,
        updated_date: Optional[datetime] = None,
    ):
        self.pk = pk
        self.sender_profile = sender_profile
        self.recipient_profile = recipient_profile
        self.sender_amount = sender_amount
        self.recipient_amount = recipient_amount
        self.punica_fee = punica_fee
        self.crypto_fee = crypto_fee
        self.crypto_to_cash_fee = crypto_to_cash_fee
        self.created_date = created_date
        self.updated_date = updated_date
