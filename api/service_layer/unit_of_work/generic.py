import abc

from adapters.repositories.db import bank_accounts, companies, invoices, operations, users


class AbstractUnitOfWork(abc.ABC):
    users: users.UsersDBRepository
    companies: companies.CompanyDBRepository
    companies_m2m_contractors: companies.CompanyM2MContractorDBRepository
    companies_m2m_employers: companies.CompanyM2MEmployerDBRepository
    invite_users_to_companies: companies.InviteUserToCompanyDBRepository
    recipient_bank_accounts: bank_accounts.RecipientBankAccountDBRepository
    sender_bank_accounts: bank_accounts.SenderBankAccountDBRepository
    invoices: invoices.InvoicesDBRepository
    invoice_items: invoices.InvoiceItemsDBRepository
    operations: operations.OperationsDBRepository

    @abc.abstractmethod
    async def clean(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError
