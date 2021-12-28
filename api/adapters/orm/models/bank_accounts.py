from tortoise import fields

from .generic import AbstractModel


class AbstractSenderBankAccount(AbstractModel):

    sender_bank_account_type = fields.CharField(max_length=16)
    sender_currency = fields.CharField(max_length=3)
    sender_country_alpha3 = fields.CharField(max_length=3)

    class Meta:
        abstract = True


class AbstractRecipientBankAccount(AbstractModel):

    recipient_bank_account_type = fields.CharField(max_length=16)
    recipient_currency = fields.CharField(max_length=3)
    recipient_country_alpha3 = fields.CharField(max_length=3)

    class Meta:
        abstract = True


class SenderBankAccount(AbstractSenderBankAccount):
    sender_owner_company = fields.ForeignKeyField("models.Company", related_name="sender_bank_accounts", null=True)
    sender_owner_user = fields.ForeignKeyField("models.User", related_name="sender_bank_accounts", null=True)


class RecipientBankAccount(AbstractRecipientBankAccount):
    recipient_owner_company = fields.ForeignKeyField(
        "models.Company", related_name="recipient_bank_accounts", null=True
    )
    recipient_owner_user = fields.ForeignKeyField("models.User", related_name="recipient_bank_accounts", null=True)
