from decimal import Decimal
from typing import Optional

from pydantic.types import UUID4

from ..models.operations import Country, Currency
from .generic import AbstractCommand


class RetrieveAccountsCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class CreateAccountCommand(AbstractCommand):
    currency: Currency
    country_alpha3: Country


class UpdateAccountCommand(AbstractCommand):
    currency: Optional[Currency]
    country_alpha3: Optional[Country]


class RetrieveAccountCommand(AbstractCommand):
    pk: UUID4


class DeleteAccountCommand(AbstractCommand):
    pk: UUID4


class RetrieveRecipientAccountsCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class RetrieveOperationsCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class CreateOperationCommand(AbstractCommand):
    sender_account: Optional[CreateAccountCommand]
    sender_amount: Optional[Decimal]

    recipient_account: Optional[CreateAccountCommand]
    recipient_amount: Optional[Decimal]


class UpdateOperationCommand(AbstractCommand):
    sender_account: Optional[CreateAccountCommand]
    sender_amount: Optional[Decimal]

    recipient_account: Optional[CreateAccountCommand]
    recipient_amount: Optional[Decimal]


class RetrieveOperationCommand(AbstractCommand):
    pk: UUID4
