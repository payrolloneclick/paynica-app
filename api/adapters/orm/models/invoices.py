from tortoise import fields

from .generic import AbstractModel


class Invoice(AbstractModel):
    created_by = fields.ForeignKeyField("models.User", related_name="invoices")
    for_company = fields.ForeignKeyField("models.Company", related_name="invoices")

    # user bank account
    recipient_account = fields.ForeignKeyField("models.RecipientBankAccount", related_name="invoices")

    # company bank account
    sender_account = fields.ForeignKeyField("models.SenderBankAccount", related_name="invoices", null=True)

    operation = fields.ForeignKeyField("models.Operation", related_name="invoices", null=True)


class InvoiceItem(AbstractModel):
    invoice = fields.ForeignKeyField("models.Invoice", related_name="invoice_items")
    amount = fields.DecimalField(max_digits=9, decimal_places=2)
    quantity = fields.IntField()
    descripion = fields.TextField(null=True)
