from .generic import AbstractSession


class FakeSession(AbstractSession):
    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    async def close(self) -> None:
        pass
