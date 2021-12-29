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
from domain.types import TPrimaryKey
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_company_id, get_current_user_id

router = APIRouter(
    prefix="/employer/invoices",
    tags=["employer-invoices"],
)


@router.get("", response_model=List[InvoiceResponse])
async def get_invoices(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get invoices list for authenticated employer."""
    command = EmployerInvoiceListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return [InvoiceResponse(**o.dict()) for o in result]


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get a company for authenticated employer."""
    command = EmployerInvoiceRetrieveCommand(invoice_id=invoice_id)
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return InvoiceResponse(**result.dict())


@router.post("/{invoice_id}/pay", response_model=InvoiceResponse)
async def pay_invoice(
    invoice_id: TPrimaryKey,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Pay an invoice for authenticated employer."""
    command = EmployerInvoicePayCommand(invoice_id=invoice_id)
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return InvoiceResponse(**result.dict())


@router.patch("/bulk/pay", response_model=List[InvoiceResponse])
async def pay_bulk_invoices(
    command: EmployerBulkInvoicePayCommand,
    current_employer_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Pay bulk of invoices for authenticated employer."""
    result = await bus.handler(
        command,
        current_user_id=current_employer_id,
        current_company_id=current_company_id,
    )
    return [InvoiceResponse(**o.dict()) for o in result]
