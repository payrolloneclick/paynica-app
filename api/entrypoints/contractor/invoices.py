from typing import List

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.contractor.invoices import (
    ContractorInvoiceCreateCommand,
    ContractorInvoiceDeleteCommand,
    ContractorInvoiceListCommand,
    ContractorInvoiceRetrieveCommand,
    ContractorInvoiceUpdateCommand,
)
from domain.responses.invoices import InvoiceResponse
from domain.types import TPrimaryKey

from ..dependencies import get_current_contractor_pk

router = APIRouter(
    prefix="/contractor/invoices",
    tags=["contractor-invoices"],
)


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Get invoices list for authenticated contractor."""
    result = await bus.handler(ContractorInvoiceListCommand(), current_user_pk=current_contractor_pk)
    return [InvoiceResponse(**o.dict()) for o in result]


@router.get("/{invoice_pk}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Get an invoice for authenticated contractor."""
    command = ContractorInvoiceRetrieveCommand(invoice_pk=invoice_pk)
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return InvoiceResponse(**result.dict())


@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    command: ContractorInvoiceCreateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Create an invoice for authenticated contractor."""
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return InvoiceResponse(**result.dict())


@router.patch("/{invoice_pk}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_pk: TPrimaryKey,
    command: ContractorInvoiceUpdateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Update an invoice for authenticated contractor."""
    command.invoice_pk = invoice_pk
    result = await bus.handler(command, current_user_pk=current_contractor_pk)
    return InvoiceResponse(**result.dict())


@router.delete("/{invoice_pk}")
async def delete_invoice(
    invoice_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_contractor_pk),
):
    """Delete/inactivate an invoice for authenticated contractor."""
    command = ContractorInvoiceDeleteCommand(invoice_pk=invoice_pk)
    await bus.handler(command, current_user_pk=current_contractor_pk)
