from typing import List, Optional

from fastapi import APIRouter, Depends

from bootstrap import bus
from domain.commands.employer.invoices import (
    EmployerBulkInvoicePayCommand,
    EmployerInvoiceListCommand,
    EmployerInvoicePayCommand,
    EmployerInvoiceRetrieveCommand,
)
from domain.responses.invoices import InvoiceResponse
from domain.types import TPrimaryKey, TSortByDirection
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_user_pk

router = APIRouter(
    prefix="/employer/invoices",
    tags=["employer-invoices"],
)


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(
    company_pk: Optional[TPrimaryKey] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by_field: Optional[str] = None,
    sort_by_direction: Optional[TSortByDirection] = TSortByDirection.DESC,
    current_employer_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Get invoices list for authenticated employer."""
    command = EmployerInvoiceListCommand()
    command.for_company_pk = company_pk
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by_field = sort_by_field
    command.sort_by_direction = sort_by_direction
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return [InvoiceResponse(**o.dict()) for o in result]


@router.get("/{invoice_pk}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Get a company for authenticated employer."""
    command = EmployerInvoiceRetrieveCommand(invoice_pk=invoice_pk)
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return InvoiceResponse(**result.dict())


@router.post("/{invoice_pk}/pay", response_model=InvoiceResponse)
async def pay_invoice(
    invoice_pk: TPrimaryKey,
    current_employer_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Pay an invoice for authenticated employer."""
    command = EmployerInvoicePayCommand(invoice_pk=invoice_pk)
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return InvoiceResponse(**result.dict())


@router.patch("/bulk/pay", response_model=List[InvoiceResponse])
async def pay_bulk_invoices(
    command: EmployerBulkInvoicePayCommand,
    current_employer_pk: TPrimaryKey = Depends(get_current_user_pk),
):
    """Pay bulk of invoices for authenticated employer."""
    result = await bus.handler(command, current_user_pk=current_employer_pk)
    return [InvoiceResponse(**o.dict()) for o in result]
