from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class ContractorCompanyListCommand(AbstractListCommand):
    pass


class ContractorCompanyRetrieveCommand(AbstractCommand):
    company_id: TPrimaryKey


class ContractorCompanyLeaveCommand(AbstractCommand):
    company_id: TPrimaryKey
