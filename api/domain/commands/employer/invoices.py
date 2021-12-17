from typing import List, Optional

from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerInvoiceListCommand(AbstractListCommand):
    for_company_pk: Optional[TPrimaryKey]


class EmployerInvoiceRetrieveCommand(AbstractCommand):
    invoice_pk: TPrimaryKey


class EmployerInvoicePayCommand(AbstractCommand):
    invoice_pk: TPrimaryKey


class EmployerBulkInvoicePayCommand(AbstractCommand):
    invoice_pks: List[TPrimaryKey]
