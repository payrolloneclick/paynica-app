from ..fake.companies import (
    CompanyFakeRepository,
    CompanyM2MContractorFakeRepository,
    CompanyM2MEmployerFakeRepository,
    InviteUserToCompanyFakeRepository,
)


# TODO
class CompanyDBRepository(CompanyFakeRepository):
    pass


# TODO
class CompanyM2MContractorDBRepository(CompanyM2MContractorFakeRepository):
    pass


# TODO
class CompanyM2MEmployerDBRepository(CompanyM2MEmployerFakeRepository):
    pass


# TODO
class InviteUserToCompanyDBRepository(InviteUserToCompanyFakeRepository):
    pass
