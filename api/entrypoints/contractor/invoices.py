from typing import List, Optional

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
from settings import DEFAULT_LIMIT

from ..dependencies import get_current_company_pk, get_current_user_pk

router = APIRouter(
    prefix="/contractor/invoices",
    tags=["contractor-invoices"],
)


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(
    company_pk: Optional[TPrimaryKey] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
    current_company_pk: TPrimaryKey = Depends(get_current_company_pk),
):
    """Get invoices list for authenticated contractor."""
    command = ContractorInvoiceListCommand()
    command.for_company_pk = company_pk
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(
        command,
        current_user_pk=current_contractor_pk,
        current_company_pk=current_company_pk,
    )
    return [InvoiceResponse(**o.dict()) for o in result]


@router.get("/{invoice_pk}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
    current_company_pk: TPrimaryKey = Depends(get_current_company_pk),
):
    """Get an invoice for authenticated contractor."""
    command = ContractorInvoiceRetrieveCommand(invoice_pk=invoice_pk)
    result = await bus.handler(
        command,
        current_user_pk=current_contractor_pk,
        current_company_pk=current_company_pk,
    )
    return InvoiceResponse(**result.dict())


@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    command: ContractorInvoiceCreateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
    current_company_pk: TPrimaryKey = Depends(get_current_company_pk),
):
    """Create an invoice for authenticated contractor."""
    result = await bus.handler(
        command,
        current_user_pk=current_contractor_pk,
        current_company_pk=current_company_pk,
    )
    return InvoiceResponse(**result.dict())


@router.patch("/{invoice_pk}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_pk: TPrimaryKey,
    command: ContractorInvoiceUpdateCommand,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
    current_company_pk: TPrimaryKey = Depends(get_current_company_pk),
):
    """Update an invoice for authenticated contractor."""
    command.invoice_pk = invoice_pk
    result = await bus.handler(
        command,
        current_user_pk=current_contractor_pk,
        current_company_pk=current_company_pk,
    )
    return InvoiceResponse(**result.dict())


@router.delete("/{invoice_pk}")
async def delete_invoice(
    invoice_pk: TPrimaryKey,
    current_contractor_pk: TPrimaryKey = Depends(get_current_user_pk),
    current_company_pk: TPrimaryKey = Depends(get_current_company_pk),
):
    """Delete/inactivate an invoice for authenticated contractor."""
    command = ContractorInvoiceDeleteCommand(invoice_pk=invoice_pk)
    await bus.handler(
        command,
        current_user_pk=current_contractor_pk,
        current_company_pk=current_company_pk,
    )
