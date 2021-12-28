from typing import List

from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerInvoiceListCommand(AbstractListCommand):
    pass


class EmployerInvoiceRetrieveCommand(AbstractCommand):
    invoice_pk: TPrimaryKey


class EmployerInvoicePayCommand(AbstractCommand):
    invoice_pk: TPrimaryKey


class EmployerBulkInvoicePayCommand(AbstractCommand):
    invoice_pks: List[TPrimaryKey]
