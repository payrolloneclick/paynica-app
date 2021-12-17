from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class ContractorOperationListCommand(AbstractListCommand):
    operation_owner_company_pk: TPrimaryKey


class ContractorOperationRetrieveCommand(AbstractCommand):
    operation_pk: TPrimaryKey
