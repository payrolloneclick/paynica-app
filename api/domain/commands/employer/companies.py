from typing import Optional

from pydantic.types import constr

from domain.types import TPrimaryKey

from ..generic import AbstractCommand


class EmployerCompanyListCommand(AbstractCommand):
    offset: Optional[int] = 0
    limit: Optional[int] = 25


class EmployerCompanyCreateCommand(AbstractCommand):
    name: constr(strip_whitespace=True)


class EmployerCompanyRetrieveCommand(AbstractCommand):
    company_pk: TPrimaryKey


class EmployerCompanyUpdateCommand(AbstractCommand):
    company_pk: Optional[TPrimaryKey]
    name: Optional[constr(strip_whitespace=True)]


class EmployerCompanyDeleteCommand(AbstractCommand):
    company_pk: TPrimaryKey


class EmployerCompanyLeaveCommand(AbstractCommand):
    company_pk: TPrimaryKey
