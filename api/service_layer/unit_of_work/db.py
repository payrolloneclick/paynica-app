from adapters.repositories.db import bank_accounts, companies, invoices, operations, users
from adapters.repositories.session.db import DBSession
from settings import DATABASE_URI

from .generic import AbstractUnitOfWork


class DBUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session=None):
        self.session = session or DBSession(DATABASE_URI)

    async def __aenter__(self):
        self.users = users.UsersDBRepository(self.session)
        self.companies = companies.CompanyDBRepository(self.session)
        self.companies_m2m_contractors = companies.CompanyM2MContractorDBRepository(self.session)
        self.companies_m2m_employers = companies.CompanyM2MEmployerDBRepository(self.session)
        self.recipient_bank_accounts = bank_accounts.RecipientBankAccountDBRepository(self.session)
        self.sender_bank_accounts = bank_accounts.SenderBankAccountDBRepository(self.session)
        self.invoices = invoices.InvoicesDBRepository(self.session)
        self.operations = operations.OperationsDBRepository(self.session)

    async def __aexit__(self, *args, **kwargs):
        await super().__aexit__(*args, **kwargs)

    async def clean(self):
        await self.session.clean()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
