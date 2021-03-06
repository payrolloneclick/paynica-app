import abc


class AbstractSmsAdapter(abc.ABC):
    @abc.abstractmethod
    async def clean(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, phone, sms):
        raise NotImplementedError
