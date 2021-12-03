from adapters.email.email import EmailAdapter
from adapters.sms.sms import SmsAdapter
from service_layer.messagebus.messagebus import MessageBus
from service_layer.unit_of_work.db import DBUnitOfWork


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def init(self, *args, **kwargs):
        pass


class Bootstrap(Singleton):
    def init(self, *args, **kwargs):
        uow = DBUnitOfWork()
        sms_adapter = SmsAdapter()
        email_adapter = EmailAdapter()
        return MessageBus(
            uow=uow,
            sms_adapter=sms_adapter,
            email_adapter=email_adapter,
        )


bus = Bootstrap().init()
