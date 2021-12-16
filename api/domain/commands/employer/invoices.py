from typing import List, Optional

from domain.types import TPrimaryKey

from ..generic import AbstractCommand


class EmployerInvoiceListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class EmployerInvoiceRetrieveCommand(AbstractCommand):
    invoice_pk: TPrimaryKey


class EmployerInvoicePayCommand(AbstractCommand):
    invoice_pk: TPrimaryKey


class EmployerBulkInvoicePayCommand(AbstractCommand):
    invoice_pks: List[TPrimaryKey]
