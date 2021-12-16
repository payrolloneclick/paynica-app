from typing import Optional

from domain.types import TPrimaryKey

from ..generic import AbstractCommand


class ContractorCompanyListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class ContractorCompanyRetrieveCommand(AbstractCommand):
    company_pk: TPrimaryKey


class ContractorCompanyLeaveCommand(AbstractCommand):
    company_pk: TPrimaryKey
