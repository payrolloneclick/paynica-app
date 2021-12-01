from adapters.repositories.fake import operations, users

from .generic import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        self.users = users.UsersFakeRepository(self.session)
        self.sender_profiles = operations.SenderProfilesFakeRepository(self.session)
        self.recipient_profiles = operations.RecipientProfilesFakeRepository(self.session)
        self.operations = operations.OperationsFakeRepository(self.session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
