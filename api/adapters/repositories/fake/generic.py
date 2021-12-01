from typing import List, Optional

from pydantic.main import BaseModel
from pydantic.types import UUID4

from ..exceptions import MultipleObjectsReturned, ObjectAlreadyExists, ObjectDoesNotExist
from ..generic import AbstractRepository
from ..session.generic import AbstractSession


class AbstractFakeRepository(AbstractRepository):
    def __init__(self, session: AbstractSession) -> None:
        self.session = session
        self._objs = {}

    async def add(self, obj: BaseModel) -> None:
        if obj.pk in self._objs:
            raise ObjectAlreadyExists
        self._objs[obj.pk] = obj

    async def get(self, **kwargs) -> BaseModel:
        objs = await self.filter(**kwargs)
        if not objs:
            raise ObjectDoesNotExist(detail=f"{self.__class__.__name__} object associated with {kwargs} doesn't exist.")
        if len(objs) > 1:
            raise MultipleObjectsReturned(
                detail=f"There are multiple {self.__class__.__name__} objects associated with {kwargs}."
            )
        return objs[0]

    async def filter(self, **kwargs) -> List[BaseModel]:
        objs = filter(lambda o: o, self._objs)
        for key in kwargs:
            objs = filter(lambda o: getattr(o, key) == kwargs[key], objs)
        return [o for o in objs]

    async def all(self) -> List[BaseModel]:
        return self._objs

    async def update(self, obj: BaseModel) -> None:
        if obj.pk not in self._objs:
            raise ObjectDoesNotExist
        self._objs[obj.pk] = obj

    async def delete(self, pk: UUID4) -> UUID4:
        if pk not in self._objs:
            raise ObjectDoesNotExist
        if pk in self._objs:
            del self._objs[pk]
        return pk
