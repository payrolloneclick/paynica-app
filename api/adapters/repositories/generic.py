import abc

from pydantic.main import BaseModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, obj) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, **kwargs) -> BaseModel:
        raise NotImplementedError
