from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import inquires, orders
from utils.token_handler import response_get_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    response_get_token()
    # response_get_websocket()
    # key = load_websocket_file()
    print(f'start server')
    yield
    print(f'stop server')

app = FastAPI(title="Demian", version="0.0.1", lifespan=lifespan, debug=True)

app.include_router(inquires.router)
app.include_router(orders.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}