import abc

from api.adapters.repositories.generic import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    users: AbstractRepository
    sender_profiles: AbstractRepository
    recipient_profiles: AbstractRepository
    operations: AbstractRepository

    async def __aexit__(self, *args, **kwargs):
        # rollback does nothing in case we run commit into context manager before exit
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError
