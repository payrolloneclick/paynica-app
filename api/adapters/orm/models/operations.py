from tortoise import fields

from .bank_accounts import AbstractRecipientBankAccount, AbstractSenderBankAccount
from .generic import AbstractModel


class Operation(AbstractSenderBankAccount, AbstractRecipientBankAccount, AbstractModel):
    operation_owner_company = fields.ForeignKeyField("models.Company", related_name="operations")

    operation_sender_user = fields.ForeignKeyField("models.User", related_name="sender_operations")
    operation_recipient_user = fields.ForeignKeyField("models.User", related_name="recipient_operations")

    sender_account = fields.ForeignKeyField("models.SenderBankAccount", related_name="operations", null=True)
    sender_amount = fields.DecimalField(max_digits=9, decimal_places=2, null=True)

    recipient_account = fields.ForeignKeyField("models.RecipientBankAccount", related_name="operations", null=True)
    recipient_amount = fields.DecimalField(max_digits=9, decimal_places=2, null=True)

    status = fields.CharField(max_length=16)
    our_fee = fields.DecimalField(max_digits=9, decimal_places=2, null=True)
    provider_fee = fields.DecimalField(max_digits=9, decimal_places=2, null=True)
