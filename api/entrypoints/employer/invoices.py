from typing import List

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.employer.invoices import (
    EmployerBulkInvoicePayCommand,
    EmployerInvoiceListCommand,
    EmployerInvoicePayCommand,
    EmployerInvoiceRetrieveCommand,
)
from domain.responses.invoices import InvoiceResponse
from domain.types import TPrimaryKey

from ..dependencies import get_current_employer_pk

router = APIRouter(
    prefix="/employer/invoices",
    tags=["employer-invoices"],
)


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get invoices list for authenticated employer."""
    result = await bus.handler(EmployerInvoiceListCommand(), current_user_pk=current_employer_pk)
    return [InvoiceResponse(**o.dict()) for o in result]


@router.get("/{invoice_pk}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Get a company for authenticated employer."""
    command = EmployerInvoiceRetrieveCommand(invoice_pk=invoice_pk)
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return InvoiceResponse(**result.dict())


@router.post("/{invoice_pk}/pay", response_model=InvoiceResponse)
async def pay_invoice(
    invoice_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Pay an invoice for authenticated employer."""
    command = EmployerInvoicePayCommand(invoice_pk=invoice_pk)
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return InvoiceResponse(**result.dict())


@router.patch("/bulk/pay", response_model=List[InvoiceResponse])
async def pay_bulk_invoices(
    command: EmployerBulkInvoicePayCommand,
    current_employer_pk: TPrimaryKey = Depends(get_current_employer_pk),
):
    """Pay bulk of invoices for authenticated employer."""
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return [InvoiceResponse(**o.dict()) for o in result]