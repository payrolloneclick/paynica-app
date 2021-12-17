from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerOperationListCommand(AbstractListCommand):
    operation_owner_company_pk: TPrimaryKey


class EmployerOperationRetrieveCommand(AbstractCommand):
    operation_pk: TPrimaryKey
