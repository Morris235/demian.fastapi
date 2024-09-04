from fastapi import FastAPI
from routers import inquires

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await response_get_token()
#     yield

app = FastAPI()

app.include_router(inquires.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}