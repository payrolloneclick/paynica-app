from typing import Optional

from domain.types import TCountry, TCurrency, TPrimaryKey

from ..generic import AbstractCommand


class ContractorRecipientBankAccountListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class ContractorRecipientBankAccountCreateCommand(AbstractCommand):
    recipient_currency: TCurrency
    recipient_country_alpha3: TCountry


class ContractorRecipientBankAccountRetrieveCommand(AbstractCommand):
    recipient_bank_account_pk: TPrimaryKey


class ContractorRecipientBankAccountUpdateCommand(AbstractCommand):
    recipient_bank_account_pk: TPrimaryKey
    recipient_currency: Optional[TCurrency]
    recipient_country_alpha3: Optional[TCountry]


class ContractorRecipientBankAccountDeleteCommand(AbstractCommand):
    recipient_bank_account_pk: TPrimaryKey
