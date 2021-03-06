from typing import Optional

from domain.types import TBankAccountType, TCountry, TCurrency, TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerSenderBankAccountListCommand(AbstractListCommand):
    pass


class EmployerSenderBankAccountCreateCommand(AbstractCommand):
    sender_bank_account_type: TBankAccountType
    sender_currency: TCurrency
    sender_country_alpha3: TCountry


class EmployerSenderBankAccountRetrieveCommand(AbstractCommand):
    sender_bank_account_id: TPrimaryKey


class EmployerSenderBankAccountUpdateCommand(AbstractCommand):
    sender_bank_account_id: TPrimaryKey
    sender_currency: Optional[TCurrency]
    sender_country_alpha3: Optional[TCountry]


class EmployerSenderBankAccountDeleteCommand(AbstractCommand):
    sender_bank_account_id: TPrimaryKey
