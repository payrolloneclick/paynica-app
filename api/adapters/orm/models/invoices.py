from tortoise import fields

from domain.models.invoices import Invoice, InvoiceItem

from .generic import ORMAbstractModel


class ORMInvoice(ORMAbstractModel):
    created_by = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="invoices",
    )
    for_company = fields.ForeignKeyField(
        "models.ORMCompany",
        related_name="invoices",
    )

    # user bank account
    recipient_account = fields.ForeignKeyField(
        "models.ORMRecipientBankAccount",
        related_name="invoices",
    )

    # company bank account
    sender_account = fields.ForeignKeyField(
        "models.ORMSenderBankAccount",
        related_name="invoices",
        null=True,
    )

    operation = fields.ForeignKeyField(
        "models.ORMOperation",
        related_name="invoices",
        null=True,
    )

    class Meta:
        pydantic_cls = Invoice


class ORMInvoiceItem(ORMAbstractModel):
    invoice = fields.ForeignKeyField(
        "models.ORMInvoice",
        related_name="invoice_items",
    )
    amount = fields.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    quantity = fields.IntField()
    descripion = fields.TextField(null=True)

    class Meta:
        pydantic_cls = InvoiceItem
