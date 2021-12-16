import secrets
from typing import Optional

from pydantic.types import constr

from domain.types import TEmail, TInvitationCode, TPrimaryKey

from .generic import AbstractModel
from .users import User


class Company(AbstractModel):
    name: constr(strip_whitespace=True)
    owner_pk: TPrimaryKey
    owner: Optional[User]


class CompanyM2MEmployer(AbstractModel):
    company_pk: TPrimaryKey
    company: Optional[Company]
    employer_pk: TPrimaryKey
    employer: Optional[User]


class CompanyM2MContractor(AbstractModel):
    company_pk: TPrimaryKey
    company: Optional[Company]
    contractor_pk: TPrimaryKey
    contractor: Optional[User]


class InviteUserToCompany(AbstractModel):
    sender_pk: TPrimaryKey
    sender: Optional[User]
    company_pk: TPrimaryKey
    company: Optional[Company]
    email: TEmail
    invitation_code: TInvitationCode

    async def randomly_set_invitation_code(self, length: int = 16) -> None:
        self.invitation_code = secrets.token_hex(length)
