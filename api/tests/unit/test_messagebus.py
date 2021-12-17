import pytest

from adapters.email.fake import FakeEmailAdapter
from adapters.sms.fake import FakeSmsAdapter
from admin.resources.generic import AdminResources
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
    admin_resources = AdminResources(uow)
    bus = MessageBus(
        uow=uow,
        sms_adapter=sms_adapter,
        email_adapter=email_adapter,
        admin_resources=admin_resources,
    )
    with pytest.raises(Exception):
        await bus.handler(InvalidMessage())
