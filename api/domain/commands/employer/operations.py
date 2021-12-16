from typing import Optional

from domain.types import TPrimaryKey

from ..generic import AbstractCommand


class EmployerOperationListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class EmployerOperationRetrieveCommand(AbstractCommand):
    operation_pk: TPrimaryKey
