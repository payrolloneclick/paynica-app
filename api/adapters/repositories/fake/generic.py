from pydantic.types import UUID4

from ..exceptions import ObjectAlreadyExists, ObjectDoesNotExist
from ..generic import AbstractRepository


class AbstractFakeRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
        self._objs = []

    async def add(self, obj) -> None:
        if obj.pk in self._objs:
            raise ObjectAlreadyExists
        self._objs[obj.pk] = obj

    async def get(self, pk: UUID4):
        if pk not in self._objs:
            raise ObjectDoesNotExist
        return self._objs.get(pk)

    async def all(self):
        return self._objs

    async def update(self, obj) -> None:
        if obj.pk not in self._objs:
            raise ObjectDoesNotExist
        self._objs[obj.pk] = obj

    async def delete(self, pk: UUID4) -> UUID4:
        if pk not in self._objs:
            raise ObjectDoesNotExist
        if pk in self._objs:
            del self._objs[pk]
        return pk
