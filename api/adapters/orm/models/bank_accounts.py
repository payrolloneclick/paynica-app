from tortoise import fields

from domain.models.bank_accounts import RecipientBankAccount, SenderBankAccount

from .generic import ORMAbstractModel


class ORMAbstractSenderBankAccount(ORMAbstractModel):

    sender_bank_account_type = fields.CharField(max_length=16)
    sender_currency = fields.CharField(max_length=3)
    sender_country_alpha3 = fields.CharField(max_length=3)

    class Meta:
        abstract = True


class ORMAbstractRecipientBankAccount(ORMAbstractModel):

    recipient_bank_account_type = fields.CharField(max_length=16)
    recipient_currency = fields.CharField(max_length=3)
    recipient_country_alpha3 = fields.CharField(max_length=3)

    class Meta:
        abstract = True


class ORMSenderBankAccount(ORMAbstractSenderBankAccount):
    sender_owner_company = fields.ForeignKeyField(
        "models.ORMCompany",
        related_name="sender_bank_accounts",
        null=True,
    )
    sender_owner_user = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="sender_bank_accounts",
        null=True,
    )

    class Meta:
        pydantic_cls = SenderBankAccount


class ORMRecipientBankAccount(ORMAbstractRecipientBankAccount):
    recipient_owner_company = fields.ForeignKeyField(
        "models.ORMCompany",
        related_name="recipient_bank_accounts",
        null=True,
    )
    recipient_owner_user = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="recipient_bank_accounts",
        null=True,
    )

    class Meta:
        pydantic_cls = RecipientBankAccount
