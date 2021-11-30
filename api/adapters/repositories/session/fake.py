from .generic import AbstractSession


class FakeSession(AbstractSession):
    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def close(self):
        pass
