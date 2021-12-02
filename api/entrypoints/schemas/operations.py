from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from domain.models.operations import Country

from domain.models.operations import Currency


class AccountCreateRequest(BaseModel):
    currency: Currency
    country_alpha3: Country


class AccountUpdateRequest(BaseModel):
    currency: Optional[Currency]
    country_alpha3: Optional[Country]


class AccountResponse(BaseModel):
    currency: Currency
    country_alpha3: Country


class OperationCreateRequest(BaseModel):
    sender_account: Optional[AccountCreateRequest]
    sender_amount: Optional[Decimal]

    recipient_account: Optional[AccountCreateRequest]
    recipient_amount: Optional[Decimal]


class OperationUpdateRequest(BaseModel):
    sender_account: Optional[AccountCreateRequest]
    sender_amount: Optional[Decimal]

    recipient_account: Optional[AccountCreateRequest]
    recipient_amount: Optional[Decimal]


class OperationResponse(BaseModel):
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
