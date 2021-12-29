from tortoise import Tortoise
from tortoise.backends.asyncpg.client import TransactionWrapper
from tortoise.exceptions import TransactionManagementError as ORMTransactionManagementError
from tortoise.transactions import current_transaction_map

from adapters.repositories.db import bank_accounts, companies, invoices, operations, users
from adapters.repositories.session.db import DBSession

from .generic import AbstractUnitOfWork


class DBUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session=None):
        self.session = session or DBSession()
        self.wrapped_connection = None
        self.connection_name = None
        self.token = None

    async def __aenter__(self):
        connection = Tortoise.get_connection("default")
        self.wrapped_connection = TransactionWrapper(connection)
        current_transaction = current_transaction_map[self.wrapped_connection.connection_name]
        self.token = current_transaction.set(self.wrapped_connection)
        self.wrapped_connection._connection = await self.wrapped_connection._parent._pool.acquire()
        await self.session.start(self.wrapped_connection)

        self.users = users.UsersDBRepository(self.session)
        self.companies = companies.CompanyDBRepository(self.session)
        self.companies_m2m_contractors = companies.CompanyM2MContractorDBRepository(self.session)
        self.companies_m2m_employers = companies.CompanyM2MEmployerDBRepository(self.session)
        self.invite_users_to_companies = companies.InviteUserToCompanyDBRepository(self.session)
        self.recipient_bank_accounts = bank_accounts.RecipientBankAccountDBRepository(self.session)
        self.sender_bank_accounts = bank_accounts.SenderBankAccountDBRepository(self.session)
        self.invoices = invoices.InvoicesDBRepository(self.session)
        self.invoice_items = invoices.InvoiceItemsDBRepository(self.session)
        self.operations = operations.OperationsDBRepository(self.session)

    async def __aexit__(self, exc_type: any, exc_val: any, exc_tb: any) -> None:
        if not self.wrapped_connection or not self.token:
            return
        if not self.wrapped_connection._finalized:
            if exc_type:
                # Can't rollback a transaction that already failed.
                if exc_type is not ORMTransactionManagementError:
                    await self.rollback()
            else:
                await self.commit()
        current_transaction_map[self.wrapped_connection.connection_name].reset(self.token)
        if self.wrapped_connection._parent._pool:
            await self.wrapped_connection._parent._pool.release(self.wrapped_connection._connection)

    async def clean(self):
        await self.session.clean()

    async def commit(self):
        if self.wrapped_connection:
            await self.session.commit(self.wrapped_connection)

    async def rollback(self):
        if self.wrapped_connection:
            await self.session.rollback(self.wrapped_connection)
