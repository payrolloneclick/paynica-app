from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

import jwt

from adapters.email.email import EmailAdapter
from adapters.sms.sms import SmsAdapter
from domain.commands.users import (
    ChangePasswordCommand,
    GenerateAccessTokenCommand,
    GenerateEmailCodeCommand,
    GenerateInvitationCodeCommand,
    GeneratePhoneCodeCommand,
    GenerateResetPasswordCodeCommand,
    ProfileDeleteCommand,
    ProfileRetrieveCommand,
    ProfileUpdateCommand,
    RefreshAccessTokenCommand,
    ResetPasswordCommand,
    SendEmailCodeByEmailCommand,
    SendInvitationCodeByEmailCommand,
    SendPhoneCodeBySmsCommand,
    SendResetPasswordCodeByEmailCommand,
    SignUpUserCommand,
    VerifyEmailCodeCommand,
    VerifyInvitationCodeAndInviteUserToCompanyCommand,
    VerifyPhoneCodeCommand,
)
from domain.models.companies import CompanyM2MContractor, CompanyM2MEmployer, InviteUserToCompany
from domain.models.users import User
from domain.responses.users import GenerateAccessTokenResponse, RefreshAccessTokenResponse
from domain.types import TPrimaryKey, TRole
from service_layer.unit_of_work.db import DBUnitOfWork
from settings import JWT_ACCESS_TOKEN_EXPIRED_AT, JWT_REFRESH_TOKEN_EXPIRED_AT, JWT_SECRET_KEY

from ..exceptions import PermissionDeniedException, ValidationException


async def generate_access_token_handler(
    message: GenerateAccessTokenCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> GenerateAccessTokenResponse:
    async with uow:
        user = await uow.users.get(email=message.email)
        if not user.is_active:
            raise PermissionDeniedException(detail="Please finish signup process for this user")
        if not await user.verify_password(message.password) or not user.is_active:
            raise PermissionDeniedException(detail="Invalid credentials")

    now = datetime.utcnow()
    refresh_token_expired_at = now + timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRED_AT)
    refresh_token = jwt.encode(
        {
            "user_pk": str(user.pk),
            "refresh_token_expired_at": refresh_token_expired_at.isoformat(),
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )

    access_token_expired_at = now + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRED_AT)
    access_token = jwt.encode(
        {
            "user_pk": str(user.pk),
            "access_token_expired_at": access_token_expired_at.isoformat(),
            "refresh_token": refresh_token,
            "refresh_token_expired_at": refresh_token_expired_at.isoformat(),
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )

    return GenerateAccessTokenResponse(
        access_token=access_token,
        access_token_expired_at=access_token_expired_at,
        refresh_token=refresh_token,
        refresh_token_expired_at=refresh_token_expired_at,
    )


async def refresh_access_token_handler(
    message: RefreshAccessTokenCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> RefreshAccessTokenResponse:
    try:
        decoded_refresh_token = jwt.decode(message.refresh_token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise PermissionDeniedException(detail="Invalid refresh token")

    refresh_token_expired_at = decoded_refresh_token.get("refresh_token_expired_at")
    user_pk = decoded_refresh_token.get("user_pk")
    if not refresh_token_expired_at or not user_pk:
        raise PermissionDeniedException(detail="Invalid payload for refresh token")

    expired_at = datetime.fromisoformat(refresh_token_expired_at)
    now = datetime.utcnow()
    if expired_at < now:
        raise PermissionDeniedException(detail="Expired refresh token")

    async with uow:
        user = await uow.users.get(pk=UUID(user_pk))
        if not user.is_active:
            raise PermissionDeniedException(detail="Inactive user. Please finish sign up process.")
        # TODO get user and salt/token from user to control jwt

    access_token_expired_at = now + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRED_AT)
    access_token = jwt.encode(
        {
            "user_pk": str(user.pk),
            "access_token_expired_at": access_token_expired_at.isoformat(),
            "refresh_token": message.refresh_token,
            "refresh_token_expired_at": refresh_token_expired_at,
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )
    return RefreshAccessTokenResponse(
        access_token=access_token,
        access_token_expired_at=access_token_expired_at,
    )


async def signup_user_handler(
    message: SignUpUserCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        if await uow.users.exists(email=message.email, is_active=True):
            raise ValidationException(detail="Active user with this email already exists")

        other_role = TRole.CONTRACTOR if message.role == TRole.EMPLOYER else TRole.EMPLOYER
        if await uow.users.exists(email=message.email, role=other_role):
            raise ValidationException(detail="User with other role and this email already exists")

        user = await uow.users.first(email=message.email, role=message.role, is_active=False)
        if user:
            await user.set_password(message.password)
            await uow.users.update(user)
        else:
            user = User(
                pk=uuid4(),
                created_date=datetime.utcnow(),
                email=message.email,
                role=message.role,
                is_active=False,
                is_onboarded=False,
            )
            await user.set_password(message.password)
            await uow.users.add(user)
        await uow.commit()
    return user


async def generate_email_code_handler(
    message: GenerateEmailCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(email=message.email)
        if user.is_email_verified:
            raise ValidationException(detail="Email is already verified")
        await user.randomly_set_email_code()
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_email_code_by_email_handler(
    message: SendEmailCodeByEmailCommand,
    email_adapter: Optional[EmailAdapter] = None,
) -> None:
    await email_adapter.send(
        message.user.email,
        "Email verification",
        f"Verification code: {message.user.email_code}",
    )


async def verify_email_code_handler(
    message: VerifyEmailCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(email_code=message.email_code)
        user.is_email_verified = True
        user.is_active = True
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user


async def generate_phone_code_handler(
    message: GeneratePhoneCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(phone=message.phone)
        if user.is_phone_verified:
            raise ValidationException(detail="Phone is already verified")
        await user.randomly_set_phone_code()
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_phone_code_by_sms_handler(
    message: SendPhoneCodeBySmsCommand,
    sms_adapter: Optional[SmsAdapter] = None,
) -> None:
    await sms_adapter.send(
        message.user.phone,
        f"Code: {message.user.phone_code}",
    )


async def verify_phone_code_handler(
    message: VerifyPhoneCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(phone_code=message.phone_code)
        user.is_phone_verified = True
        user.is_active = True
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user


async def generate_reset_password_code_handler(
    message: GenerateResetPasswordCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        user = await uow.users.get(email=message.email)
        await user.randomly_set_password_code()
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user


async def send_reset_password_code_handler(
    message: SendResetPasswordCodeByEmailCommand,
    email_adapter: Optional[EmailAdapter] = None,
) -> None:
    await email_adapter.send(
        message.user.email,
        "Reset password",
        f"Verification code: {message.user.password_code}",
    )


async def reset_password_handler(
    message: ResetPasswordCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> Optional[User]:
    async with uow:
        user = await uow.users.get(password_code=message.password_code)
        await user.set_password(message.password)
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user


async def generate_invitation_code_handler(
    message: GenerateInvitationCodeCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> InviteUserToCompany:
    invite_user_to_company = InviteUserToCompany(
        pk=uuid4(),
        sender_pk=current_user_pk,
        company_pk=message.company_pk,
        email=message.email,
        created_date=datetime.utcnow(),
    )
    async with uow:
        if not await uow.companies.exists(pk=message.company_pk):
            raise ValidationException(detail="Company with this company_pk doesn't exist")
        sender_user = await uow.users.first(pk=current_user_pk)
        if sender_user.role == TRole.EMPLOYER and not await uow.companies_m2m_employers.exists(
            company_pk=message.company_pk, employer_pk=sender_user.pk
        ):
            raise ValidationException(detail="Company with this company_pk doesn't have authenticated current user")
        if sender_user.role == TRole.CONTRACTOR and not await uow.companies_m2m_contractors.exists(
            company_pk=message.company_pk, contractor_pk=sender_user.pk
        ):
            raise ValidationException(detail="Company with this company_pk doesn't have authenticated current user")

        user = await uow.users.first(email=invite_user_to_company.email)
        if not user:
            user = User(
                pk=uuid4(),
                created_date=datetime.utcnow(),
                email=message.email,
                role=TRole.CONTRACTOR,
                is_active=False,
                is_onboarded=False,
            )
            await uow.users.add(user)
        if user.role == TRole.EMPLOYER and await uow.companies_m2m_employers.exists(
            company_pk=message.company_pk, employer_pk=user.pk
        ):
            raise ValidationException(detail="User is already in this company")
        if user.role == TRole.CONTRACTOR and await uow.companies_m2m_contractors.exists(
            company_pk=message.company_pk, contractor_pk=user.pk
        ):
            raise ValidationException(detail="User is already in this company")
        if await uow.invite_users_to_companies.exists(email=message.email, company_pk=message.company_pk):
            raise ValidationException(detail="Invitation with this email and company_pk already exists")
        await invite_user_to_company.randomly_set_invitation_code()
        await uow.invite_users_to_companies.add(invite_user_to_company)
        await uow.commit()
    return invite_user_to_company


async def send_invitation_code_by_email_handler(
    message: SendInvitationCodeByEmailCommand,
    email_adapter: Optional[EmailAdapter] = None,
) -> None:
    await email_adapter.send(
        message.invite_user_to_company.email,
        "Invitation",
        f"Invitation code: {message.invite_user_to_company.invitation_code}",
    )


async def invite_user_handler(
    message: VerifyInvitationCodeAndInviteUserToCompanyCommand,
    uow: Optional[DBUnitOfWork] = None,
) -> User:
    async with uow:
        invite_user_to_company = await uow.invite_users_to_companies.get(invitation_code=message.invitation_code)
        user = await uow.users.get(email=invite_user_to_company.email)
        if user.role == TRole.EMPLOYER:
            company_m2m_employer = CompanyM2MEmployer(
                pk=uuid4(),
                created_date=datetime.utcnow(),
                company_pk=invite_user_to_company.company_pk,
                employer_pk=user.pk,
            )
            await uow.companies_m2m_employers.add(company_m2m_employer)
        if user.role == TRole.CONTRACTOR:
            company_m2m_contractor = CompanyM2MContractor(
                pk=uuid4(),
                created_date=datetime.utcnow(),
                company_pk=invite_user_to_company.company_pk,
                contractor_pk=user.pk,
            )
            await uow.companies_m2m_contractors.add(company_m2m_contractor)
        await uow.invite_users_to_companies.delete(invite_user_to_company.pk)
        await uow.commit()
    return user


async def profile_update_handler(
    message: ProfileUpdateCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> User:
    async with uow:
        user = await uow.users.get(pk=current_user_pk)
        if message.first_name:
            user.first_name = message.first_name
        if message.last_name:
            user.last_name = message.last_name
        if message.is_onboarded:
            user.is_onboarded = message.is_onboarded
        if message.email:
            if await uow.users.exists(email=message.email):
                raise ValidationException(detail="User with this email already exists")
            if message.email != user.email:
                user.is_email_verified = False
            user.email = message.email
        if message.phone:
            if await uow.users.exists(phone=message.phone):
                raise ValidationException(detail="User with this phone already exists")
            if message.phone != user.phone:
                user.is_phone_verified = False
            user.phone = message.phone
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user


async def profile_retrieve_handler(
    message: ProfileRetrieveCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> User:
    async with uow:
        user = await uow.users.get(pk=current_user_pk, is_active=True)
    return user


async def profile_delete_handler(
    message: ProfileDeleteCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> TPrimaryKey:
    async with uow:
        await uow.users.delete(current_user_pk)
        await uow.commit()
    return current_user_pk


async def change_password_handler(
    message: ChangePasswordCommand,
    uow: Optional[DBUnitOfWork] = None,
    current_user_pk: Optional[TPrimaryKey] = None,
) -> User:
    async with uow:
        user = await uow.users.get(pk=current_user_pk)
        await user.set_password(message.password)
        user.updated_date = datetime.utcnow()
        await uow.users.update(user)
        await uow.commit()
    return user
