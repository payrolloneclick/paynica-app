from .generic import AbstractSession


# TODO
class DBSession(AbstractSession):
    def __init__(self, uri: str) -> None:
        self.uri = uri

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    async def close(self) -> None:
        pass
