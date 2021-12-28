import pytest

from adapters.email.fake import FakeEmailAdapter
from adapters.sms.fake import FakeSmsAdapter
from domain.commands.generic import AbstractCommand
from service_layer.messagebus.messagebus import MessageBus
from service_layer.unit_of_work.fake import FakeUnitOfWork


class InvalidMessage(AbstractCommand):
    pass


@pytest.mark.asyncio
async def test_messagebus():
    uow = FakeUnitOfWork()
    sms_adapter = FakeSmsAdapter()
    email_adapter = FakeEmailAdapter()
    bus = MessageBus(
        uow=uow,
        sms_adapter=sms_adapter,
        email_adapter=email_adapter,
    )
    with pytest.raises(Exception):
        await bus.handler(InvalidMessage())
