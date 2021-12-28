import abc
from typing import Optional

from pydantic.types import UUID4

from adapters.email.email import EmailAdapter
from adapters.repositories.generic import AbstractRepository
from adapters.sms.sms import SmsAdapter
from service_layer.handlers.generic import AbstractMessage
from service_layer.unit_of_work.db import DBUnitOfWork


class AbstractMessageBus(abc.ABC):
    uow: DBUnitOfWork
    sms_adapter: SmsAdapter
    email_adapter: EmailAdapter

    @abc.abstractmethod
    async def clean(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def handler(self, message: AbstractMessage, current_user_pk: Optional[UUID4] = None) -> AbstractRepository:
        raise NotImplementedError
