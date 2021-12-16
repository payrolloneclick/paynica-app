from typing import List, Optional

from domain.models.users import User

from .generic import AbstractFakeRepository


class UsersFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[User]:
        return await super().all()

    async def filter(self, **kwargs) -> List[User]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> User:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[User]:
        return await super().first(**kwargs)

    async def add(self, obj: User) -> None:
        return await super().add(obj)
