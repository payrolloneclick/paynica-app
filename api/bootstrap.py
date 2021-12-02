from adapters.email.email import EmailAdapter
from adapters.sms.sms import SmsAdapter
from service_layer.unit_of_work.db import DBUnitOfWork


uow = DBUnitOfWork()
sms_adapter = SmsAdapter()
email_adapter = EmailAdapter()
