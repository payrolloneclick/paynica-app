import abc


class AbstractEmailAdapter(abc.ABC):
    @abc.abstractmethod
    async def send(self, email: str, subject: str, body: str) -> None:
        raise NotImplementedError
