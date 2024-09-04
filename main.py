from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.v1.oauth import delete_token
from routers import inquires
from utils.token_handler import response_get_token, response_delete_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    token_key: str = response_get_token()
    print(f'start server : get token -> {token_key}')
    yield
    response_delete_token()
    print(f'stop server : delete token -> {token_key}')

app = FastAPI(title="Demian", version="0.0.1", lifespan=lifespan)

app.include_router(inquires.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}