from typing import List, Optional

from pydantic.main import BaseModel
from pydantic.types import UUID4

from settings import DEFAULT_LIMIT

from ..exceptions import MultipleObjectsReturned, ObjectAlreadyExists, ObjectDoesNotExist
from ..generic import AbstractRepository
from ..session.generic import AbstractSession


class AbstractFakeRepository(AbstractRepository):
    def __init__(self, session: AbstractSession) -> None:
        self.session = session
        if self.__class__.__name__ not in self.session.objects:
            self.session.objects[self.__class__.__name__] = {}

    async def add(self, obj: BaseModel) -> None:
        if obj.pk in self.session.objects:
            raise ObjectAlreadyExists
        print(obj)
        self.session.objects[self.__class__.__name__][obj.pk] = obj

    async def get(self, **kwargs) -> BaseModel:
        objs = await self.filter(**kwargs)
        if not objs:
            raise ObjectDoesNotExist(detail=f"{self.__class__.__name__} object associated with {kwargs} doesn't exist.")
        if len(objs) > 1:
            raise MultipleObjectsReturned(
                detail=f"There are multiple {self.__class__.__name__} objects associated with {kwargs}."
            )
        return objs[0]

    async def list(
        self,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        **kwargs,
    ) -> List[BaseModel]:
        objs = await self.filter(**kwargs)
        # TODO search, sort_by
        return objs[offset:limit]

    async def filter(self, **kwargs) -> List[BaseModel]:
        def filter_by(obj, key, value):
            if "__in" in key:
                key = key.replace("__in", "")
                return getattr(obj, key) in value
            return getattr(obj, key) == value

        objs = await self.all()
        for key in kwargs:
            objs = [o for o in objs if filter_by(o, key, kwargs[key])]
        return objs

    async def first(self, **kwargs) -> Optional[BaseModel]:
        objs = await self.filter(**kwargs)
        if objs:
            return objs[0]
        return None

    async def count(self, **kwargs) -> int:
        objs = await self.filter(**kwargs)
        return len(objs)

    async def exists(self, **kwargs) -> bool:
        count = await self.count(**kwargs)
        return count > 0

    async def all(self) -> List[BaseModel]:
        return [o for o in self.session.objects[self.__class__.__name__].values()]

    async def update(self, obj: BaseModel) -> None:
        if obj.pk not in self.session.objects[self.__class__.__name__]:
            raise ObjectDoesNotExist
        print(obj)
        self.session.objects[self.__class__.__name__][obj.pk] = obj

    async def delete(self, pk: UUID4) -> UUID4:
        if pk not in self.session.objects[self.__class__.__name__]:
            raise ObjectDoesNotExist
        if pk in self.session.objects[self.__class__.__name__]:
            del self.session.objects[self.__class__.__name__][pk]
        return pk
