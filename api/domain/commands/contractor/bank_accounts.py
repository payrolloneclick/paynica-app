from typing import Optional

from domain.types import TBankAccountType, TCountry, TCurrency, TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class ContractorRecipientBankAccountListCommand(AbstractListCommand):
    pass


class ContractorRecipientBankAccountCreateCommand(AbstractCommand):
    recipient_bank_account_type: TBankAccountType
    recipient_currency: TCurrency
    recipient_country_alpha3: TCountry


class ContractorRecipientBankAccountRetrieveCommand(AbstractCommand):
    recipient_bank_account_id: TPrimaryKey


class ContractorRecipientBankAccountUpdateCommand(AbstractCommand):
    recipient_bank_account_id: TPrimaryKey
    recipient_currency: Optional[TCurrency]
    recipient_country_alpha3: Optional[TCountry]


class ContractorRecipientBankAccountDeleteCommand(AbstractCommand):
    recipient_bank_account_id: TPrimaryKey
