from adapters.repositories.fake import bank_accounts, companies, invoices, operations, users
from adapters.repositories.session.fake import FakeSession

from .generic import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session=None):
        self.session = session or FakeSession()
        self.transaction = None

    async def __aenter__(self):
        await self.session.start(None)
        self.users = users.UsersFakeRepository(self.session)
        self.companies = companies.CompanyFakeRepository(self.session)
        self.companies_m2m_contractors = companies.CompanyM2MContractorFakeRepository(self.session)
        self.companies_m2m_employers = companies.CompanyM2MEmployerFakeRepository(self.session)
        self.invite_users_to_companies = companies.InviteUserToCompanyFakeRepository(self.session)
        self.recipient_bank_accounts = bank_accounts.RecipientBankAccountFakeRepository(self.session)
        self.sender_bank_accounts = bank_accounts.SenderBankAccountFakeRepository(self.session)
        self.invoices = invoices.InvoicesFakeRepository(self.session)
        self.invoice_items = invoices.InvoiceItemsFakeRepository(self.session)
        self.operations = operations.OperationsFakeRepository(self.session)

    async def __aexit__(self, *args, **kwargs):
        await self.rollback()

    async def clean(self):
        await self.session.clean()

    async def commit(self):
        if self.transaction:
            await self.session.commit(self.transaction)

    async def rollback(self):
        if self.transaction:
            await self.session.rollback(self.transaction)
