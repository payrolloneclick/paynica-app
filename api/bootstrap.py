from adapters.email.email import EmailAdapter
from adapters.email.fake import FakeEmailAdapter
from adapters.sms.fake import FakeSmsAdapter
from adapters.sms.sms import SmsAdapter
from generic import Singleton
from service_layer.messagebus.messagebus import MessageBus
from service_layer.unit_of_work.db import DBUnitOfWork
from service_layer.unit_of_work.fake import FakeUnitOfWork
from settings import TEST_ENV


class FakeBootstrap(Singleton):
    def init(self):
        uow = FakeUnitOfWork()
        sms_adapter = FakeSmsAdapter()
        email_adapter = FakeEmailAdapter()
        return MessageBus(
            uow=uow,
            sms_adapter=sms_adapter,
            email_adapter=email_adapter,
        )


class Bootstrap(Singleton):
    def init(self):
        uow = DBUnitOfWork()
        sms_adapter = SmsAdapter()
        email_adapter = EmailAdapter()
        return MessageBus(
            uow=uow,
            sms_adapter=sms_adapter,
            email_adapter=email_adapter,
        )


if TEST_ENV:
    bus = FakeBootstrap().init()
else:
    bus = Bootstrap().init()
