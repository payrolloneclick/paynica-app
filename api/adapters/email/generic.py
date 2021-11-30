import abc


class AbstractEmailAdapter(abc.ABC):
    @abc.abstractmethod
    async def send(self, email, subject, body):
        raise NotImplementedError
