from adapters.email.email import EmailAdapter
from adapters.email.fake import FakeEmailAdapter
from adapters.sms.fake import FakeSmsAdapter
from adapters.sms.sms import SmsAdapter
from admin.resources import resources as admin_resources
from admin.resources.generic import AdminResources
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
        admin_resources = AdminResources(uow)
        return MessageBus(
            uow=uow,
            sms_adapter=sms_adapter,
            email_adapter=email_adapter,
            admin_resources=admin_resources,
        )


class Bootstrap(Singleton):
    def init(self):
        uow = DBUnitOfWork()
        sms_adapter = SmsAdapter()
        email_adapter = EmailAdapter()
        admin_resources = AdminResources()
        return MessageBus(
            uow=uow,
            sms_adapter=sms_adapter,
            email_adapter=email_adapter,
            admin_resources=admin_resources,
        )


if TEST_ENV:
    bus = FakeBootstrap().init()
else:
    bus = Bootstrap().init()


bus.admin_resources.register_resource(admin_resources.UserAdmin)
bus.admin_resources.register_resource(admin_resources.CompanyAdmin)
bus.admin_resources.register_resource(admin_resources.CompanyM2MEmployerAdmin)
bus.admin_resources.register_resource(admin_resources.CompanyM2MContractorAdmin)
bus.admin_resources.register_resource(admin_resources.InviteUserToCompanyAdmin)
bus.admin_resources.register_resource(admin_resources.SenderBankAccountAdmin)
bus.admin_resources.register_resource(admin_resources.RecipientBankAccountAdmin)
bus.admin_resources.register_resource(admin_resources.InvoiceAdmin)
bus.admin_resources.register_resource(admin_resources.OperationAdmin)
