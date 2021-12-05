from adapters.repositories.fake import operations, users
from adapters.repositories.session.fake import FakeSession
from settings import DATABASE_URI

from .generic import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session=None):
        self.session = session or FakeSession(DATABASE_URI)

    async def __aenter__(self):
        self.users = users.UsersFakeRepository(self.session)
        self.accounts = operations.AccountFakeRepository(self.session)
        self.operations = operations.OperationsFakeRepository(self.session)

    async def clean(self):
        await self.session.clean()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
