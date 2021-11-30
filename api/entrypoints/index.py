import aiohttp
from fastapi import APIRouter

router = APIRouter(
    prefix="/",
    tags=["index"],
)


@router.get("/")
async def index():
    async with aiohttp.ClientSession("https://api.blockchain.com") as session:
        async with session.get("/v3/exchange/accounts") as resp:
            print(resp.status)
            print(await resp.text())

    return {"message": "Hello World"}
