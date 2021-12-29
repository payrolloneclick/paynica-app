from tortoise import fields

from domain.models.companies import Company, CompanyM2MContractor, CompanyM2MEmployer, InviteUserToCompany

from .generic import ORMAbstractModel


class ORMCompany(ORMAbstractModel):
    name = fields.CharField(max_length=255)
    owner = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="companies",
    )

    class Meta:
        pydantic_cls = Company


class ORMCompanyM2MEmployer(ORMAbstractModel):
    company = fields.ForeignKeyField(
        "models.ORMCompany",
        related_name="companies_m2m_employers",
    )
    employer = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="companies_m2m_employers",
    )

    class Meta:
        unique_together = ("company", "employer")
        pydantic_cls = CompanyM2MEmployer


class ORMCompanyM2MContractor(ORMAbstractModel):
    company = fields.ForeignKeyField(
        "models.ORMCompany",
        related_name="companies_m2m_contractors",
    )
    contractor = fields.ForeignKeyField(
        "models.ORMUser",
        related_name="companies_m2m_contractors",
    )

    class Meta:
        unique_together = ("company", "contractor")
        pydantic_cls = CompanyM2MContractor


class ORMInviteUserToCompany(ORMAbstractModel):
    sender = fields.ForeignKeyField("models.ORMUser", related_name="invites")
    company = fields.ForeignKeyField(
        "models.ORMCompany",
        related_name="invites",
        null=True,
    )
    email = fields.CharField(max_length=255)
    invitation_code = fields.CharField(max_length=255)

    class Meta:
        pydantic_cls = InviteUserToCompany
