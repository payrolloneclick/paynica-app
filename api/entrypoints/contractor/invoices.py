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

from ..dependencies import get_current_company_id, get_current_user_id

router = APIRouter(
    prefix="/contractor/invoices",
    tags=["contractor-invoices"],
)


@router.get("", response_model=List[InvoiceResponse])
async def get_invoices(
    offset: Optional[int] = 0,
    limit: Optional[int] = DEFAULT_LIMIT,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get invoices list for authenticated contractor."""
    command = ContractorInvoiceListCommand()
    command.offset = offset
    command.limit = limit
    command.search = search
    command.sort_by = sort_by
    result = await bus.handler(
        command,
        current_user_id=current_contractor_id,
        current_company_id=current_company_id,
    )
    return [InvoiceResponse(**o.dict()) for o in result]


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: TPrimaryKey,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Get an invoice for authenticated contractor."""
    command = ContractorInvoiceRetrieveCommand(invoice_id=invoice_id)
    result = await bus.handler(
        command,
        current_user_id=current_contractor_id,
        current_company_id=current_company_id,
    )
    return InvoiceResponse(**result.dict())


@router.post("", response_model=InvoiceResponse)
async def create_invoice(
    command: ContractorInvoiceCreateCommand,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Create an invoice for authenticated contractor."""
    result = await bus.handler(
        command,
        current_user_id=current_contractor_id,
        current_company_id=current_company_id,
    )
    return InvoiceResponse(**result.dict())


@router.patch("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: TPrimaryKey,
    command: ContractorInvoiceUpdateCommand,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Update an invoice for authenticated contractor."""
    command.invoice_id = invoice_id
    result = await bus.handler(
        command,
        current_user_id=current_contractor_id,
        current_company_id=current_company_id,
    )
    return InvoiceResponse(**result.dict())


@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: TPrimaryKey,
    current_contractor_id: TPrimaryKey = Depends(get_current_user_id),
    current_company_id: TPrimaryKey = Depends(get_current_company_id),
):
    """Delete/inactivate an invoice for authenticated contractor."""
    command = ContractorInvoiceDeleteCommand(invoice_id=invoice_id)
    await bus.handler(
        command,
        current_user_id=current_contractor_id,
        current_company_id=current_company_id,
    )
