from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from domain.commands.contractor.invoices import (
    ContractorInvoiceCreateCommand,
    ContractorInvoiceDeleteCommand,
    ContractorInvoiceListCommand,
    ContractorInvoiceRetrieveCommand,
    ContractorInvoiceUpdateCommand,
)
from domain.models.invoices import Invoice, InvoiceItem
from domain.types import TPrimaryKey, TRole
from service_layer.exceptions import PermissionDeniedException
from service_layer.unit_of_work.db import DBUnitOfWork

from ..permissions import has_role


@has_role(role=TRole.CONTRACTOR)
async def invoice_list_handler(
    message: ContractorInvoiceListCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> List[Invoice]:
    async with uow:
        invoices = await uow.invoices.list(
            search=message.search,
            sort_by=message.sort_by,
            limit=message.limit,
            offset=message.offset,
            created_by_pk=current_user_pk,
            for_company_pk=current_company_pk,
        )
    return invoices


@has_role(role=TRole.CONTRACTOR)
async def invoice_retrieve_handler(
    message: ContractorInvoiceRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> Invoice:
    async with uow:
        invoice = await uow.invoices.get(
            pk=message.recipient_bank_account_pk,
            created_by_pk=current_user_pk,
            for_company_pk=current_company_pk,
        )
        invoice.items = await uow.invoice_items.filter(invoice_pk=invoice.pk)
    return invoice


@has_role(role=TRole.CONTRACTOR)
async def invoice_create_handler(
    message: ContractorInvoiceCreateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> Invoice:
    async with uow:
        invoice = Invoice(
            pk=uuid4(),
            created_date=datetime.utcnow(),
            created_by_pk=current_user_pk,
            for_company_pk=current_company_pk,
            recipient_account_pk=message.recipient_account_pk,
        )
        await uow.invoices.add(invoice)
        invoice_items = []
        for item in message.items:
            invoice_item = InvoiceItem(
                pk=uuid4(),
                created_date=datetime.utcnow(),
                invoice_pk=invoice.pk,
                amount=item.amount,
                quantity=item.quantity,
                description=item.description,
            )
            await uow.invoice_items.add(invoice_item)
            invoice_items.append(invoice_item)
        invoice.items = invoice_items
        await uow.commit()
    return invoice


@has_role(role=TRole.CONTRACTOR)
async def invoice_update_handler(
    message: ContractorInvoiceUpdateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> Invoice:
    async with uow:
        invoice = await uow.invoices.get(
            pk=message.recipient_bank_account_pk,
            created_by_pk=current_user_pk,
            for_company_pk=current_company_pk,
        )
        if message.recipient_account_pk:
            invoice.recipient_account_pk = message.recipient_account_pk
        invoice.updated_date = datetime.utcnow()
        await uow.invoices.update(invoice)
        invoice_items = await uow.invoice_items.filter(invoice_pk=message.invoice_pk)
        for invoice_item in invoice_items:
            message_invoice_item = next((i for i in message.items if i.pk == invoice_item.pk), None)
            if message_invoice_item:
                if message_invoice_item.amount is not None:
                    invoice_item.amount = message_invoice_item.amount
                if message_invoice_item.quantity is not None:
                    invoice_item.quantity = message_invoice_item.quantity
                if message_invoice_item.description is not None:
                    invoice_item.description = message_invoice_item.description
                invoice_item.updated_date = datetime.utcnow()
                uow.invoice_items.update(invoice_item)
            else:
                uow.invoice_items.delete(invoice_item.pk)
        for message_invoice_item in message.items:
            invoice_item = next((i for i in invoice_items if i.pk == message_invoice_item.pk), None)
            if not invoice_item:
                invoice_item = InvoiceItem(
                    pk=uuid4(),
                    created_date=datetime.utcnow(),
                    invoice_pk=invoice.pk,
                    amount=message_invoice_item.amount,
                    quantity=message_invoice_item.quantity,
                    description=message_invoice_item.description,
                )
                uow.invoice_items.add(invoice_item)
        await uow.commit()
    return invoice


@has_role(role=TRole.CONTRACTOR)
async def invoice_delete_handler(
    message: ContractorInvoiceDeleteCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
    current_company_pk: Optional[TPrimaryKey] = None,
) -> None:
    async with uow:
        if not await uow.invoices.exists(
            pk=message.invoice_pk,
            created_by_pk=current_user_pk,
            for_company_pk=current_company_pk,
        ):
            raise PermissionDeniedException(detail="User has no access to delete this invoice")
        invoice_items = await uow.invoice_items.filter(invoice_pk=message.invoice_pk)
        for item in invoice_items:
            await uow.invoice_items.delete(item.pk)
        await uow.invoices.delete(message.invoice_pk)
        await uow.commit()
