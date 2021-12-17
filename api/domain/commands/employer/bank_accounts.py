from typing import Optional

from domain.types import TCountry, TCurrency, TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerSenderBankAccountListCommand(AbstractListCommand):
    sender_owner_company_pk: TPrimaryKey


class EmployerSenderBankAccountCreateCommand(AbstractCommand):
    sender_owner_company_pk: TPrimaryKey
    sender_currency: TCurrency
    sender_country_alpha3: TCountry


class EmployerSenderBankAccountRetrieveCommand(AbstractCommand):
    sender_bank_account_pk: TPrimaryKey


class EmployerSenderBankAccountUpdateCommand(AbstractCommand):
    sender_bank_account_pk: TPrimaryKey
    sender_currency: Optional[TCurrency]
    sender_country_alpha3: Optional[TCountry]


class EmployerSenderBankAccountDeleteCommand(AbstractCommand):
    sender_bank_account_pk: TPrimaryKey
