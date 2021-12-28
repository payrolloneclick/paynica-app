from typing import List, Optional

from domain.models.companies import Company, CompanyM2MContractor, CompanyM2MEmployer, InviteUserToCompany
from settings import DEFAULT_LIMIT

from .generic import AbstractFakeRepository


class CompanyFakeRepository(AbstractFakeRepository):
    async def list(
        self,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        **kwargs,
    ) -> List[Company]:
        return await super().list(search=search, sort_by=sort_by, offset=offset, limit=limit, **kwargs)

    async def all(self) -> List[Company]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Company]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Company:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[Company]:
        return await super().first(**kwargs)

    async def add(self, obj: Company) -> None:
        return await super().add(obj)


class CompanyM2MContractorFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[CompanyM2MContractor]:
        return await super().all()

    async def filter(self, **kwargs) -> List[CompanyM2MContractor]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> CompanyM2MContractor:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[CompanyM2MContractor]:
        return await super().first(**kwargs)

    async def add(self, obj: CompanyM2MContractor) -> None:
        return await super().add(obj)


class CompanyM2MEmployerFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[CompanyM2MEmployer]:
        return await super().all()

    async def filter(self, **kwargs) -> List[CompanyM2MEmployer]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> CompanyM2MEmployer:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[CompanyM2MEmployer]:
        return await super().first(**kwargs)

    async def add(self, obj: CompanyM2MEmployer) -> None:
        return await super().add(obj)


class InviteUserToCompanyFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[InviteUserToCompany]:
        return await super().all()

    async def filter(self, **kwargs) -> List[InviteUserToCompany]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> InviteUserToCompany:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[InviteUserToCompany]:
        return await super().first(**kwargs)

    async def add(self, obj: InviteUserToCompany) -> None:
        return await super().add(obj)
