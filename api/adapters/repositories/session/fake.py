from .generic import AbstractSession


class FakeSession(AbstractSession):
    def __init__(self) -> None:
        self.objects = {}

    async def open(self) -> None:
        pass

    async def clean(self) -> None:
        self.objects = {}

    async def start(self, transaction: any) -> None:
        pass

    async def commit(self, transaction: any) -> None:
        pass

    async def rollback(self, transaction: any) -> None:
        pass

    async def close(self) -> None:
        pass
