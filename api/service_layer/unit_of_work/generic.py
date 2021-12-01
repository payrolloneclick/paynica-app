import abc

from adapters.repositories.db.operations import (
    OperationsDBRepository,
    RecipientProfilesDBRepository,
    SenderProfilesDBRepository,
)
from adapters.repositories.db.users import UsersDBRepository


class AbstractUnitOfWork(abc.ABC):
    users: UsersDBRepository
    sender_profiles: SenderProfilesDBRepository
    recipient_profiles: RecipientProfilesDBRepository
    operations: OperationsDBRepository

    async def __aexit__(self, *args, **kwargs):
        # rollback does nothing in case we run commit into context manager before exit
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError
