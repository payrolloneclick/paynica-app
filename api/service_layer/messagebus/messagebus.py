import inspect
from typing import Optional

from pydantic.types import UUID4

from adapters.email.generic import AbstractEmailAdapter
from adapters.sms.generic import AbstractSmsAdapter
from domain.commands import users as users_commands
from domain.commands.contractor import bank_accounts as contractor_bank_accounts_commands
from domain.commands.contractor import companies as contractor_companies_commands
from domain.commands.contractor import invoices as contractor_invoices_commands
from domain.commands.contractor import operations as contractor_operations_commands
from domain.commands.employer import bank_accounts as employer_bank_accounts_commands
from domain.commands.employer import companies as employer_companies_commands
from domain.commands.employer import invoices as employer_invoices_commands
from domain.commands.employer import operations as employer_operations_commands
from domain.responses.generic import AbstractReponse
from service_layer.exceptions import ServiceException
from service_layer.handlers import users as users_handlers
from service_layer.handlers.employer import companies as employer_companies_handlers
from service_layer.handlers.generic import AbstractMessage
from service_layer.unit_of_work.generic import AbstractUnitOfWork

from .generic import AbstractMessageBus

COMMANDS = {
    # sign in process
    users_commands.GenerateAccessTokenCommand: users_handlers.generate_access_token_handler,
    users_commands.RefreshAccessTokenCommand: users_handlers.refresh_access_token_handler,
    # sign up process
    users_commands.SignUpUserCommand: users_handlers.signup_user_handler,
    # email verification and user activation
    users_commands.GenerateEmailCodeCommand: users_handlers.generate_email_code_handler,
    users_commands.SendEmailCodeByEmailCommand: users_handlers.send_email_code_by_email_handler,
    users_commands.VerifyEmailCodeCommand: users_handlers.verify_email_code_handler,
    # phone verification and user activation
    users_commands.GeneratePhoneCodeCommand: users_handlers.generate_phone_code_handler,
    users_commands.SendPhoneCodeBySmsCommand: users_handlers.send_phone_code_by_sms_handler,
    users_commands.VerifyPhoneCodeCommand: users_handlers.verify_phone_code_handler,
    # reset password process
    users_commands.GenerateResetPasswordCodeCommand: users_handlers.generate_reset_password_code_handler,
    users_commands.SendResetPasswordCodeByEmailCommand: users_handlers.send_reset_password_code_handler,
    users_commands.ResetPasswordCommand: users_handlers.reset_password_handler,
    # invitation process
    users_commands.GenerateInvitationCodeCommand: users_handlers.generate_invitation_code_handler,
    users_commands.SendInvitationCodeByEmailCommand: users_handlers.send_invitation_code_by_email_handler,
    users_commands.VerifyInvitationCodeAndInviteUserToCompanyCommand: users_handlers.invite_user_handler,
    # profile
    users_commands.ProfileUpdateCommand: users_handlers.profile_update_handler,
    users_commands.ProfileRetrieveCommand: users_handlers.profile_retrieve_handler,
    users_commands.ProfileDeleteCommand: users_handlers.profile_delete_handler,
    users_commands.ChangePasswordCommand: users_handlers.change_password_handler,
    # companies
    employer_companies_commands.EmployerCompanyListCommand: None,
    employer_companies_commands.EmployerCompanyCreateCommand: employer_companies_handlers.company_create_handler,
    employer_companies_commands.EmployerCompanyUpdateCommand: None,
    employer_companies_commands.EmployerCompanyRetrieveCommand: None,
    employer_companies_commands.EmployerCompanyDeleteCommand: None,
    employer_companies_commands.EmployerCompanyLeaveCommand: None,
    contractor_companies_commands.ContractorCompanyListCommand: None,
    contractor_companies_commands.ContractorCompanyRetrieveCommand: None,
    contractor_companies_commands.ContractorCompanyLeaveCommand: None,
    # bank accounts
    employer_bank_accounts_commands.EmployerSenderBankAccountListCommand: None,
    employer_bank_accounts_commands.EmployerSenderBankAccountCreateCommand: None,
    employer_bank_accounts_commands.EmployerSenderBankAccountUpdateCommand: None,
    employer_bank_accounts_commands.EmployerSenderBankAccountRetrieveCommand: None,
    employer_bank_accounts_commands.EmployerSenderBankAccountDeleteCommand: None,
    contractor_bank_accounts_commands.ContractorRecipientBankAccountListCommand: None,
    contractor_bank_accounts_commands.ContractorRecipientBankAccountCreateCommand: None,
    contractor_bank_accounts_commands.ContractorRecipientBankAccountUpdateCommand: None,
    contractor_bank_accounts_commands.ContractorRecipientBankAccountRetrieveCommand: None,
    contractor_bank_accounts_commands.ContractorRecipientBankAccountDeleteCommand: None,
    # invoices
    employer_invoices_commands.EmployerInvoiceListCommand: None,
    employer_invoices_commands.EmployerInvoiceRetrieveCommand: None,
    employer_invoices_commands.EmployerInvoicePayCommand: None,
    employer_invoices_commands.EmployerBulkInvoicePayCommand: None,
    contractor_invoices_commands.ContractorInvoiceListCommand: None,
    contractor_invoices_commands.ContractorInvoiceCreateCommand: None,
    contractor_invoices_commands.ContractorInvoiceUpdateCommand: None,
    contractor_invoices_commands.ContractorInvoiceRetrieveCommand: None,
    contractor_invoices_commands.ContractorInvoiceDeleteCommand: None,
    # operations
    employer_operations_commands.EmployerOperationListCommand: None,
    employer_operations_commands.EmployerOperationRetrieveCommand: None,
    contractor_operations_commands.ContractorOperationListCommand: None,
    contractor_operations_commands.ContractorOperationRetrieveCommand: None,
}

EVENTS = {}


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

    async def clean(self) -> None:
        await self.uow.clean()
        await self.sms_adapter.clean()
        await self.email_adapter.clean()

    async def handler(self, message: AbstractMessage, current_user_pk: Optional[UUID4] = None) -> AbstractReponse:
        message_type = type(message)
        handlers = COMMANDS
        handler_fn = handlers.get(message_type)
        if not handler_fn:
            raise ServiceException(detail=f"Unsupported message type {message_type}")
        return await handler_fn(
            message,
            **filter_dependencies(
                handler_fn,
                dict(
                    uow=self.uow,
                    sms_adapter=self.sms_adapter,
                    email_adapter=self.email_adapter,
                    current_user_pk=current_user_pk,
                ),
            ),
        )
