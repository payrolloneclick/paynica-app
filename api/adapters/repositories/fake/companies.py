from typing import List

from domain.models.companies import Company, CompanyM2MContractor, CompanyM2MEmployer

from .generic import AbstractFakeRepository


class CompanyFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[Company]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Company]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Company:
        return await super().get(**kwargs)

    async def add(self, obj: Company) -> None:
        return await super().add(obj)


class CompanyM2MContractorFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[CompanyM2MContractor]:
        return await super().all()

    async def filter(self, **kwargs) -> List[CompanyM2MContractor]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> CompanyM2MContractor:
        return await super().get(**kwargs)

    async def add(self, obj: CompanyM2MContractor) -> None:
        return await super().add(obj)


class CompanyM2MEmployerFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[CompanyM2MEmployer]:
        return await super().all()

    async def filter(self, **kwargs) -> List[CompanyM2MEmployer]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> CompanyM2MEmployer:
        return await super().get(**kwargs)

    async def add(self, obj: CompanyM2MEmployer) -> None:
        return await super().add(obj)
