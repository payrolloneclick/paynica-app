from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from adapters.repositories.exceptions import ObjectDoesNotExist
from bootstrap import bus
from entrypoints.index import router as index_router
from entrypoints.operations import router as operations_router
from entrypoints.users import router as users_router
from service_layer.exceptions import PermissionDeniedException

app = FastAPI(title="Paynica", version="0.0.1")


@app.on_event("startup")
async def startup():
    await bus.uow.session.open()


@app.on_event("shutdown")
async def shutdown():
    await bus.uow.session.close()


@app.exception_handler(ObjectDoesNotExist)
async def exception_callback(request: Request, exc: ObjectDoesNotExist):
    return JSONResponse({"detail": exc.detail}, status_code=404)


@app.exception_handler(PermissionDeniedException)
async def exception_callback(request: Request, exc: PermissionDeniedException):
    return JSONResponse({"detail": exc.detail}, status_code=503)


app.include_router(index_router)
app.include_router(operations_router)
app.include_router(users_router)
