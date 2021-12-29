from typing import List

from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerInvoiceListCommand(AbstractListCommand):
    pass


class EmployerInvoiceRetrieveCommand(AbstractCommand):
    invoice_id: TPrimaryKey


class EmployerInvoicePayCommand(AbstractCommand):
    invoice_id: TPrimaryKey


class EmployerBulkInvoicePayCommand(AbstractCommand):
    invoice_ids: List[TPrimaryKey]
