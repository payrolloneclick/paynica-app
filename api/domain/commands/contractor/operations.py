from typing import Optional

from domain.types import TPrimaryKey

from ..generic import AbstractCommand


class ContractorOperationListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25
    operation_owner_company_pk: TPrimaryKey


class ContractorOperationRetrieveCommand(AbstractCommand):
    operation_pk: TPrimaryKey
