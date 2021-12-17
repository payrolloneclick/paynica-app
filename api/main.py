from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from adapters.repositories.exceptions import ObjectDoesNotExist
from admin.entrypoints import router as admin_router
from bootstrap import bus
from entrypoints.contractor.bank_accounts import router as contractor_bank_accounts_router
from entrypoints.contractor.companies import router as contractor_companies_router
from entrypoints.contractor.invoices import router as contractor_invoices_router
from entrypoints.contractor.operations import router as contractor_operations_router
from entrypoints.employer.bank_accounts import router as employer_bank_accounts_router
from entrypoints.employer.companies import router as employer_companies_router
from entrypoints.employer.invoices import router as employer_invoices_router
from entrypoints.employer.operations import router as employer_operations_router
from entrypoints.exceptions import NotAuthorizedException
from entrypoints.index import router as index_router
from entrypoints.users import router as users_router
from service_layer.exceptions import PermissionDeniedException, ValidationException

app = FastAPI(title="Paynica", version="0.0.1")
admin_app = FastAPI()


@app.on_event("startup")
async def startup():
    await bus.uow.session.open()


@app.on_event("shutdown")
async def shutdown():
    await bus.uow.session.close()


@app.exception_handler(ObjectDoesNotExist)
@admin_app.exception_handler(ObjectDoesNotExist)
async def does_not_exist_callback(request: Request, exc: ObjectDoesNotExist):
    return JSONResponse({"detail": exc.detail}, status_code=404)


@app.exception_handler(PermissionDeniedException)
@admin_app.exception_handler(PermissionDeniedException)
async def permission_denied_callback(request: Request, exc: PermissionDeniedException):
    return JSONResponse({"detail": exc.detail}, status_code=403)


@app.exception_handler(NotAuthorizedException)
@admin_app.exception_handler(NotAuthorizedException)
async def not_authorized_callback(request: Request, exc: NotAuthorizedException):
    return JSONResponse({"detail": exc.detail}, status_code=401)


@app.exception_handler(ValidationException)
@admin_app.exception_handler(ValidationException)
async def validation_callback(request: Request, exc: ValidationException):
    return JSONResponse({"detail": exc.detail}, status_code=422)


# api
app.include_router(index_router)
app.include_router(users_router)
app.include_router(employer_companies_router)
app.include_router(employer_bank_accounts_router)
app.include_router(employer_invoices_router)
app.include_router(employer_operations_router)
app.include_router(contractor_companies_router)
app.include_router(contractor_bank_accounts_router)
app.include_router(contractor_invoices_router)
app.include_router(contractor_operations_router)

# admin api
admin_app.include_router(admin_router)
app.mount("/admin", admin_app)
