from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic.types import UUID4

from adapters.email.email import EmailAdapter
from adapters.sms.sms import SmsAdapter
from domain.models.users import User
from service_layer.services import users as users_services
from service_layer.unit_of_work.db import DBUnitOfWork

from .dependencies import token_auth_scheme
from .schemas.users import UserRequest, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(token_auth_scheme)],
)


@router.post("/create-inactive-user", response_model=UserResponse)
async def create_inactive_user(user: UserRequest):
    """Create inactive user."""
    uow = DBUnitOfWork()
    user = await users_services.create_user(
        uow,
        user.first_name,
        user.last_name,
        user.email,
        user.phone,
        user.password,
    )
    return UserResponse(**user.dict())


@router.post("/send-email-code", response_model=UserResponse)
async def send_email_code(email: str, background_tasks: BackgroundTasks):
    """Send email code to verify email."""
    uow = DBUnitOfWork()
    email_adapter = EmailAdapter()
    user = await users_services.save_email_code_for_email(uow, email)
    background_tasks.add_task(users_services.send_email_code_by_email, email_adapter=email_adapter, user=user)
    return UserResponse(**user.dict())


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(email_code: str):
    """Verify email."""
    uow = DBUnitOfWork()
    user = await users_services.verify_email_code(uow, email_code)
    return UserResponse(**user.dict())


@router.post("/send-phone-code", response_model=UserResponse)
async def send_phone_code(phone: str, background_tasks: BackgroundTasks):
    """Send phone code to verify email."""
    uow = DBUnitOfWork()
    sms_adapter = SmsAdapter()
    user = await users_services.save_phone_code_for_phone(uow, phone)
    background_tasks.add_task(users_services.send_phone_code_by_sms, sms_adapter=sms_adapter, user=user)
    return UserResponse(**user.dict())


@router.post("/verify-phone", response_model=UserResponse)
async def verify_phone(phone_code: str):
    """Verify phone."""
    uow = DBUnitOfWork()
    user = await users_services.verify_phone_code(uow, phone_code)
    return UserResponse(**user.dict())


@router.post("/send-email-code", response_model=UserResponse)
async def send_password_code(email: str, background_tasks: BackgroundTasks):
    """Send password code to verify email."""
    uow = DBUnitOfWork()
    email_adapter = EmailAdapter()
    user = await users_services.save_password_code_for_email(uow, email)
    background_tasks.add_task(users_services.send_password_code_by_email, email_adapter=email_adapter, user=user)
    return UserResponse(**user.dict())


@router.post("/reset-password", response_model=UserResponse)
async def reset_password(password_code: str, password: str, repeat_password: str):
    """Verify password code and reset password."""
    uow = DBUnitOfWork()
    user = await users_services.verify_password_code_and_reset_password(
        uow,
        password_code=password_code,
        password=password,
    )
    return UserResponse(**user.dict())


@router.get("/profile", response_model=UserResponse)
async def get_profile():
    """Get profile of authenticated user."""
    # TODO
    pk = None
    uow = DBUnitOfWork()
    user = await users_services.get_active_user(uow, pk)
    return UserResponse(**user.dict())


@router.patch("/profile", response_model=UserResponse)
async def update_profile(user: UserRequest):
    """Update profile of authenticated user."""
    # TODO
    pk = None
    uow = DBUnitOfWork()
    user = await users_services.get_active_user(uow, pk)
    user = await users_services.update_user(
        uow,
        pk,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password=user.password,
    )
    return UserResponse(**user.dict())


@router.delete("/profile")
async def delete_profile():
    """Delete/inactivate profile of authenticated user."""
    pk = None
    uow = DBUnitOfWork()
    pk = await users_services.delete_user(uow, pk)
    return pk


@router.get("/recipients")
async def get_recipients():
    """Get recipients to create an operation."""
    return [{"username": "fakecurrentuser"}]
