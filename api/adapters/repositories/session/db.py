from .generic import AbstractSession


class DBSession(AbstractSession):
    def __init__(self, uri: str):
        self.uri = uri

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def close(self):
        pass
