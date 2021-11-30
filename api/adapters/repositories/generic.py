import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, reference):
        raise NotImplementedError
