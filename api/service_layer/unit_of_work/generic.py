import abc

from adapters.repositories.db.operations import AccountDBRepository, OperationsDBRepository
from adapters.repositories.db.users import UsersDBRepository


class AbstractUnitOfWork(abc.ABC):
    users: UsersDBRepository
    accounts: AccountDBRepository
    operations: OperationsDBRepository

    async def __aexit__(self, *args, **kwargs):
        # rollback does nothing in case we run commit into context manager before exit
        await self.rollback()

    @abc.abstractmethod
    async def clean(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError
