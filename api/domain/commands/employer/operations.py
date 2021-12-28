from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerOperationListCommand(AbstractListCommand):
    pass


class EmployerOperationRetrieveCommand(AbstractCommand):
    operation_pk: TPrimaryKey
