from settings import DATABASE_URI
from adapters.repositories.db import operations, users
from adapters.repositories.session.db import DBSession

from .generic import AbstractUnitOfWork


class DBUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session=None):
        self.session = session or DBSession(DATABASE_URI)

    async def __aenter__(self):
        self.users = users.UsersDBRepository(self.session)
        self.sender_profiles = operations.SenderProfilesDBRepository(self.session)
        self.recipient_profiles = operations.RecipientProfilesDBRepository(self.session)
        self.operations = operations.OperationsDBRepository(self.session)

    async def __aexit__(self, *args, **kwargs):
        await super().__aexit__(*args, **kwargs)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
