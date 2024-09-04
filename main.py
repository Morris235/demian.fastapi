from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import inquires
from utils.token_handler import response_get_token, response_delete_token
from utils.websocket_handler import response_get_websocket, load_websocket_file


@asynccontextmanager
async def lifespan(app: FastAPI):
    response_get_token()
    # response_get_websocket()
    # key = load_websocket_file()
    print(f'start server')
    yield
    response_delete_token()
    print(f'stop server')

app = FastAPI(title="Demian", version="0.0.1", lifespan=lifespan, debug=True)

app.include_router(inquires.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}