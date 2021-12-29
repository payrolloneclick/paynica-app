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
    current_user_id: Optional[TPrimaryKey] = None,
    current_company_id: Optional[TPrimaryKey] = None,
) -> List[Invoice]:
    async with uow:
        invoices = await uow.invoices.list(
            search=message.search,
            sort_by=message.sort_by,
            limit=message.limit,
            offset=message.offset,
            created_by_id=current_user_id,
            for_company_id=current_company_id,
        )
    return invoices


@has_role(role=TRole.CONTRACTOR)
async def invoice_retrieve_handler(
    message: ContractorInvoiceRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
    current_company_id: Optional[TPrimaryKey] = None,
) -> Invoice:
    async with uow:
        invoice = await uow.invoices.get(
            id=message.recipient_bank_account_id,
            created_by_id=current_user_id,
            for_company_id=current_company_id,
        )
        invoice.items = await uow.invoice_items.filter(invoice_id=invoice.id)
    return invoice


@has_role(role=TRole.CONTRACTOR)
async def invoice_create_handler(
    message: ContractorInvoiceCreateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_id: Optional[TPrimaryKey] = None,
    current_company_id: Optional[TPrimaryKey] = None,
) -> Invoice:
    async with uow:
        invoice = Invoice(
            id=uuid4(),
            created_date=datetime.utcnow(),
            created_by_id=current_user_id,
            for_company_id=current_company_id,
            recipient_account_id=message.recipient_account_id,
        )
        await uow.invoices.add(invoice)
        invoice_items = []
        for item in message.items:
            invoice_item = InvoiceItem(
                id=uuid4(),
                created_date=datetime.utcnow(),
                invoice_id=invoice.id,
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
    current_user_id: Optional[TPrimaryKey] = None,
    current_company_id: Optional[TPrimaryKey] = None,
) -> Invoice:
    async with uow:
        invoice = await uow.invoices.get(
            id=message.recipient_bank_account_id,
            created_by_id=current_user_id,
            for_company_id=current_company_id,
        )
        if message.recipient_account_id:
            invoice.recipient_account_id = message.recipient_account_id
        invoice.updated_date = datetime.utcnow()
        await uow.invoices.update(invoice)
        invoice_items = await uow.invoice_items.filter(invoice_id=message.invoice_id)
        for invoice_item in invoice_items:
            message_invoice_item = next((i for i in message.items if i.id == invoice_item.id), None)
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
                uow.invoice_items.delete(invoice_item.id)
        for message_invoice_item in message.items:
            invoice_item = next((i for i in invoice_items if i.id == message_invoice_item.id), None)
            if not invoice_item:
                invoice_item = InvoiceItem(
                    id=uuid4(),
                    created_date=datetime.utcnow(),
                    invoice_id=invoice.id,
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
    current_user_id: Optional[TPrimaryKey] = None,
    current_company_id: Optional[TPrimaryKey] = None,
) -> None:
    async with uow:
        if not await uow.invoices.exists(
            id=message.invoice_id,
            created_by_id=current_user_id,
            for_company_id=current_company_id,
        ):
            raise PermissionDeniedException(detail="User has no access to delete this invoice")
        invoice_items = await uow.invoice_items.filter(invoice_id=message.invoice_id)
        for item in invoice_items:
            await uow.invoice_items.delete(item.id)
        await uow.invoices.delete(message.invoice_id)
        await uow.commit()
