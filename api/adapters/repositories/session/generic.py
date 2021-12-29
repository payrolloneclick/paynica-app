import abc


class AbstractSession(abc.ABC):
    @abc.abstractmethod
    async def open(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def clean(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def start(self, transaction: any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def commit(self, transaction: any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self, transaction: any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
