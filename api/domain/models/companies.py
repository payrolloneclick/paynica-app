import secrets
from typing import Optional

from pydantic.types import constr

from domain.types import TEmail, TInvitationCode, TPrimaryKey

from .generic import AbstractModel
from .users import User


class Company(AbstractModel):
    name: constr(strip_whitespace=True)
    owner_id: TPrimaryKey
    owner: Optional[User]


class CompanyM2MEmployer(AbstractModel):
    company_id: TPrimaryKey
    company: Optional[Company]
    employer_id: TPrimaryKey
    employer: Optional[User]


class CompanyM2MContractor(AbstractModel):
    company_id: TPrimaryKey
    company: Optional[Company]
    contractor_id: TPrimaryKey
    contractor: Optional[User]


class InviteUserToCompany(AbstractModel):
    sender_id: TPrimaryKey
    sender: Optional[User]
    company_id: TPrimaryKey
    company: Optional[Company]
    email: TEmail
    invitation_code: Optional[TInvitationCode]

    async def randomly_set_invitation_code(self, length: int = 16) -> None:
        self.invitation_code = secrets.token_hex(length)
