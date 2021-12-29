from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class ContractorOperationListCommand(AbstractListCommand):
    pass


class ContractorOperationRetrieveCommand(AbstractCommand):
    operation_id: TPrimaryKey
