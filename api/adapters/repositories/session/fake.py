from .generic import AbstractSession


class FakeSession(AbstractSession):
    def __init__(self, uri: str) -> None:
        self.uri = uri
        self.objects = {}

    async def open(self) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    async def close(self) -> None:
        pass
