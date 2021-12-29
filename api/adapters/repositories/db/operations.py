from typing import List, Optional

from adapters.orm.models.operations import ORMOperation
from domain.models.operations import Operation
from settings import DEFAULT_LIMIT

from .generic import AbstractDBRepository


class OperationsDBRepository(AbstractDBRepository):
    orm_model_cls: type[ORMOperation] = ORMOperation

    async def list(
        self,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        **kwargs,
    ) -> List[Operation]:
        return await super().list(search=search, sort_by=sort_by, offset=offset, limit=limit, **kwargs)

    async def all(self) -> List[Operation]:
        return await super().all()

    async def filter(self, **kwargs) -> List[Operation]:
        return await super().filter(**kwargs)

    async def get(self, **kwargs) -> Operation:
        return await super().get(**kwargs)

    async def first(self, **kwargs) -> Optional[Operation]:
        return await super().first(**kwargs)

    async def add(self, obj: Operation) -> None:
        return await super().add(obj)
