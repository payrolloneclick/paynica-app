import abc
from datetime import datetime
from typing import List, Optional, Type
from uuid import uuid4

from domain.models.generic import AbstractModel
from domain.types import TPrimaryKey
from service_layer.unit_of_work.generic import AbstractUnitOfWork
from settings import DEFAULT_LIMIT


class AbstractAdminResource(abc.ABC):
    uow: AbstractUnitOfWork
    # please see service_layer/unit_of_work/generic.py and class fields here
    uow_field_name: str

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    @abc.abstractmethod
    async def list(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
    ) -> List[AbstractModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, payload: dict) -> AbstractModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, pk: TPrimaryKey, payload: dict) -> AbstractModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def retrieve(self, pk: TPrimaryKey) -> AbstractModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, pk: TPrimaryKey) -> None:
        raise NotImplementedError


class AdminResource(AbstractAdminResource):
    model_cls: Type[AbstractModel]

    async def list(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        search: Optional[str] = None,
        sort_by: List[str] = None,
    ) -> List[AbstractModel]:
        async with self.uow:
            return await getattr(self.uow, self.uow_field_name).list(
                offset=offset, limit=limit, search=search, sort_by=sort_by
            )

    async def create(self, payload: dict) -> AbstractModel:
        async with self.uow:
            obj = self.model_cls(
                pk=uuid4(),
                created_date=datetime.utcnow(),
            )
            for key, value in payload.items():
                setattr(obj, key, value)
            return await getattr(self.uow, self.uow_field_name).create(obj)

    async def update(self, pk: TPrimaryKey, payload: dict) -> AbstractModel:
        async with self.uow:
            obj = await getattr(self.uow, self.uow_field_name).get(pk=pk)
            for key, value in payload.items():
                setattr(obj, key, value)
            return await getattr(self.uow, self.uow_field_name).update(obj)

    async def retrieve(self, pk: TPrimaryKey) -> AbstractModel:
        async with self.uow:
            return await getattr(self.uow, self.uow_field_name).get(pk=pk)

    async def delete(self, pk: TPrimaryKey) -> None:
        async with self.uow:
            return await getattr(self.uow, self.uow_field_name).delete(pk=pk)


class AbstractAdminResources(abc.ABC):
    uow: AbstractUnitOfWork
    resources: dict[str, AbstractAdminResource]

    @abc.abstractmethod
    def register_resource(self, resource_cls: Type[AbstractAdminResource]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def unregister_resource(self, resource_cls: Type[AbstractAdminResource]) -> None:
        raise NotImplementedError


class AdminResources(AbstractAdminResources):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
        self.resources = {}

    def register_resource(self, resource_cls: Type[AbstractAdminResource]) -> None:
        if resource_cls.uow_field_name not in self.resources:
            self.resources[resource_cls.uow_field_name] = resource_cls(self.uow)

    def unregister_resource(self, resource_cls: Type[AbstractAdminResource]) -> None:
        self.resources.pop(resource_cls.uow_field_name, None)
