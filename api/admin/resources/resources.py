from domain.models.bank_accounts import RecipientBankAccount, SenderBankAccount
from domain.models.companies import Company, CompanyM2MContractor, CompanyM2MEmployer, InviteUserToCompany
from domain.models.invoices import Invoice
from domain.models.operations import Operation
from domain.models.users import User

from .generic import AdminResource


class UserAdmin(AdminResource):
    uow_field_name = "users"
    model_cls = User


class CompanyAdmin(AdminResource):
    uow_field_name = "companies"
    model_cls = Company


class CompanyM2MContractorAdmin(AdminResource):
    uow_field_name = "companies_m2m_contractors"
    model_cls = CompanyM2MContractor


class CompanyM2MEmployerAdmin(AdminResource):
    uow_field_name = "companies_m2m_employers"
    model_cls = CompanyM2MEmployer


class InviteUserToCompanyAdmin(AdminResource):
    uow_field_name = "invite_users_to_companies"
    model_cls = InviteUserToCompany


class SenderBankAccountAdmin(AdminResource):
    uow_field_name = "sender_bank_accounts"
    model_cls = SenderBankAccount


class RecipientBankAccountAdmin(AdminResource):
    uow_field_name = "recipient_bank_accounts"
    model_cls = RecipientBankAccount


class InvoiceAdmin(AdminResource):
    uow_field_name = "invoices"
    model_cls = Invoice


class OperationAdmin(AdminResource):
    uow_field_name = "operations"
    model_cls = Operation
