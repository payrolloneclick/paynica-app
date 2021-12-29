from tortoise import fields

from domain.models.operations import Operation

from .bank_accounts import ORMAbstractRecipientBankAccount, ORMAbstractSenderBankAccount
from .generic import ORMAbstractModel


class ORMOperation(ORMAbstractSenderBankAccount, ORMAbstractRecipientBankAccount, ORMAbstractModel):
    operation_owner_company = fields.ForeignKeyField(
        "models.ORMCompany",
        related_name="operations",
    )

    operation_sender_user = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="sender_operations",
    )
    operation_recipient_user = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="recipient_operations",
    )

    sender_account = fields.ForeignKeyField(
        "models.ORMSenderBankAccount",
        related_name="operations",
        null=True,
    )
    sender_amount = fields.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
    )

    recipient_account = fields.ForeignKeyField(
        "models.ORMRecipientBankAccount",
        related_name="operations",
        null=True,
    )
    recipient_amount = fields.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
    )

    status = fields.CharField(max_length=16)
    our_fee = fields.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
    )
    provider_fee = fields.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
    )

    class Meta:
        pydantic_cls = Operation
