from tortoise import fields

from .generic import AbstractModel


class Company(AbstractModel):
    name = fields.CharField(max_length=255)
    owner = fields.ForeignKeyField("models.User", related_name="companies")


class CompanyM2MEmployer(AbstractModel):
    company = fields.ForeignKeyField("models.Company", related_name="companies_m2m_employers")
    employer = fields.ForeignKeyField("models.User", related_name="companies_m2m_employers")

    class Meta:
        unique_together = ("company", "employer")


class CompanyM2MContractor(AbstractModel):
    company = fields.ForeignKeyField("models.Company", related_name="companies_m2m_contractors")
    contractor = fields.ForeignKeyField("models.User", related_name="companies_m2m_contractors")

    class Meta:
        unique_together = ("company", "contractor")


class InviteUserToCompany(AbstractModel):
    sender = fields.ForeignKeyField("models.User", related_name="invites")
    company = fields.ForeignKeyField("models.Company", related_name="invites", null=True)
    email = fields.CharField(max_length=255)
    invitation_code = fields.CharField(max_length=255)
