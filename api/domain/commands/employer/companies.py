from typing import Optional

from pydantic.types import constr

from domain.types import TPrimaryKey

from ..generic import AbstractCommand, AbstractListCommand


class EmployerCompanyListCommand(AbstractListCommand):
    pass


class EmployerCompanyCreateCommand(AbstractCommand):
    name: constr(strip_whitespace=True)


class EmployerCompanyRetrieveCommand(AbstractCommand):
    company_id: TPrimaryKey


class EmployerCompanyUpdateCommand(AbstractCommand):
    company_id: Optional[TPrimaryKey]
    name: Optional[constr(strip_whitespace=True)]


class EmployerCompanyDeleteCommand(AbstractCommand):
    company_id: TPrimaryKey


class EmployerCompanyLeaveCommand(AbstractCommand):
    company_id: TPrimaryKey
