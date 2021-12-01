from typing import List

from domain.models.users import User

from .generic import AbstractFakeRepository


class UsersFakeRepository(AbstractFakeRepository):
    async def all(self) -> List[User]:
        return super().all()

    async def filter(self, **kwargs) -> List[User]:
        return super().filter(**kwargs)

    async def get(self, **kwargs) -> User:
        return super().get(**kwargs)

    async def add(self, obj: User) -> None:
        return super().add(obj)
