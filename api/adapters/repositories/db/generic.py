from typing import List, Optional

from pydantic.main import BaseModel
from pydantic.types import UUID4
from tortoise.exceptions import BaseORMException as ORMBaseException
from tortoise.exceptions import DoesNotExist as ORMDoesNotExist
from tortoise.exceptions import MultipleObjectsReturned as ORMMultipleObjectsReturned
from tortoise.models import Model as ORMModel

from settings import DEFAULT_LIMIT

from ..exceptions import MultipleObjectsReturned, ObjectDoesNotExist, RepositoryException
from ..generic import AbstractRepository
from ..session.generic import AbstractSession


class AbstractDBRepository(AbstractRepository):
    orm_model_cls: type[ORMModel] = None

    def __init__(self, session: AbstractSession) -> None:
        self.session = session

    async def add(self, obj: BaseModel) -> None:
        try:
            db_obj = self.orm_model_cls()
            db_obj.from_pydantic(obj)
            await db_obj.save()
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))

    async def get(self, **kwargs) -> BaseModel:
        try:
            db_obj = await self.orm_model_cls.get(**kwargs)
        except ORMDoesNotExist:
            raise ObjectDoesNotExist(detail=f"{self.__class__.__name__} object associated with {kwargs} doesn't exist.")
        except ORMMultipleObjectsReturned:
            raise MultipleObjectsReturned(
                detail=f"There are multiple {self.__class__.__name__} objects associated with {kwargs}."
            )
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))
        return db_obj.to_pydantic()

    async def list(
        self,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = DEFAULT_LIMIT,
        **kwargs,
    ) -> List[BaseModel]:
        try:
            db_objs = await self.orm_model_cls.filter(**kwargs).offset(offset).limit(limit)
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))
        objs = [db_obj.to_pydantic() for db_obj in db_objs]
        return objs

    async def filter(self, **kwargs) -> List[BaseModel]:
        try:
            db_objs = await self.orm_model_cls.filter(**kwargs)
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))
        return [db_obj.to_pydantic() for db_obj in db_objs]

    async def first(self, **kwargs) -> Optional[BaseModel]:
        try:
            db_obj = await self.orm_model_cls.filter(**kwargs).first()
            if db_obj:
                return db_obj.to_pydantic()
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))

    async def count(self, **kwargs) -> int:
        try:
            return await self.orm_model_cls.filter(**kwargs).count()
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))

    async def exists(self, **kwargs) -> bool:
        try:
            return await self.orm_model_cls.filter(**kwargs).exists()
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))

    async def all(self) -> List[BaseModel]:
        try:
            db_objs = await self.orm_model_cls.all()
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))
        return [db_obj.to_pydantic() for db_obj in db_objs]

    async def update(self, obj: BaseModel) -> None:
        try:
            db_obj = self.orm_model_cls()
            db_obj.from_pydantic(obj)
            db_obj._saved_in_db = True
            await db_obj.save()
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))

    async def delete(self, pk: UUID4) -> UUID4:
        try:
            await self.orm_model_cls.filter(pk=pk).delete()
        except ORMBaseException as e:
            raise RepositoryException(detail=str(e))
        return pk
