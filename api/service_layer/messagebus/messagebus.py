import inspect
from typing import Optional

from pydantic.types import UUID4

from adapters.email.generic import AbstractEmailAdapter
from adapters.sms.generic import AbstractSmsAdapter
from domain.commands import operations as operations_commands
from domain.commands import users as users_commands
from domain.responses.generic import AbstractReponse
from service_layer.handlers import operations as operations_handlers
from service_layer.handlers import users as users_handlers
from service_layer.handlers.generic import AbstractMessage
from service_layer.unit_of_work.generic import AbstractUnitOfWork

from .generic import AbstractMessageBus

COMMANDS = {
    # sign up process
    users_commands.CreateUserCommand: users_handlers.create_user_handler,
    # email verification and user actvation
    users_commands.GenerateEmailCodeCommand: users_handlers.generate_email_code_handler,
    users_commands.SendEmailCodeByEmailCommand: users_handlers.send_email_code_by_email_handler,
    users_commands.VerifyEmailCodeCommand: users_handlers.verify_email_code_handler,
    # phone verification and user actvation
    users_commands.GeneratePhoneCodeCommand: users_handlers.generate_phone_code_handler,
    users_commands.SendPhoneCodeBySmsCommand: users_handlers.send_phone_code_by_sms_handler,
    users_commands.VerifyPhoneCodeCommand: users_handlers.verify_phone_code_handler,
    # reset password process
    users_commands.GenerateResetPasswordCodeCommand: users_handlers.generate_reset_password_code_handler,
    users_commands.SendResetPasswordCodeByEmailCommand: users_handlers.send_reset_password_code_handler,
    users_commands.ResetPasswordCommand: users_handlers.reset_password_handler,
    # profile
    users_commands.UpdateUserCommand: users_handlers.update_user_handler,
    users_commands.RetrieveUserCommand: users_handlers.retrieve_user_handler,
    users_commands.DeleteUserCommand: users_handlers.delete_user_handler,
    # accounts
    operations_commands.CreateAccountCommand: operations_handlers.create_account_handler,
    operations_commands.UpdateAccountCommand: operations_handlers.update_account_handler,
    operations_commands.RetrieveAccountsCommand: operations_handlers.retrieve_accounts_handler,
    operations_commands.RetrieveAccountCommand: operations_handlers.retrieve_account_handler,
    operations_commands.RetrieveRecipientAccountsCommand: operations_handlers.retrieve_recipient_accounts_handler,
    operations_commands.DeleteAccountCommand: operations_handlers.delete_account_handler,
    # operations
    operations_commands.CreateOperationCommand: operations_handlers.create_operation_handler,
    operations_commands.UpdateOperationCommand: operations_handlers.update_operation_handler,
    operations_commands.RetrieveOperationsCommand: operations_handlers.retrieve_operations_handler,
    operations_commands.RetrieveOperationCommand: operations_handlers.retrieve_operation_handler,
}


def filter_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    filtered_dependencies = {name: dependency for name, dependency in dependencies.items() if name in params}
    return filtered_dependencies


class MessageBus(AbstractMessageBus):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        sms_adapter: AbstractSmsAdapter,
        email_adapter: AbstractEmailAdapter,
    ) -> None:
        self.uow = uow
        self.sms_adapter = sms_adapter
        self.email_adapter = email_adapter

    async def handler(self, message: AbstractMessage, current_user_pk: Optional[UUID4] = None) -> AbstractReponse:
        message_type = type(message)
        handler = COMMANDS.get(message_type)
        if not handler:
            raise Exception
        return await handler(
            message,
            **filter_dependencies(
                handler,
                dict(
                    uow=self.uow,
                    sms_adapter=self.sms_adapter,
                    email_adapter=self.email_adapter,
                    current_user_pk=current_user_pk,
                ),
            )
        )
