from fastapi import FastAPI

from .entrypoints import index, operations, users

app = FastAPI()
app.include_router(index.router)
app.include_router(users.router)
app.include_router(operations.router)
