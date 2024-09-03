import json
import os.path
from datetime import datetime, timedelta
from typing import Union
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from enum import Enum


from api.v1.local.inquiry import inquire_price
from api.v1.oauth import get_token, delete_token


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    is_offer: Union[bool, None] = None


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()

TOKEN_FILE = "token_cache.json"

def second_today():
    now = datetime.now()
    start_of_data = datetime(now.year, now.month, now.day)
    end_of_day = start_of_data + timedelta(days=1) - timedelta(seconds=1)
    return (end_of_day - start_of_data).total_seconds()

def save_token_to_file(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def load_token_from_file():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return {"access_token": None, "expires_in": 0}

@app.get("/get_token")
async def response_get_token():
    token_data = load_token_from_file()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        response = get_token()
        save_token_to_file(response.json())
        print(response.text)
    return token_data["access_token"]

@app.get("/delete_token")
async def response_delete_token():
    token_data = load_token_from_file()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        return {"response" : "already deleted"}
    os.remove(TOKEN_FILE)
    response = delete_token(token_data["access_token"])
    return response

@app.get("/inquire_price")
async def response_inquire_price():
    token_data = load_token_from_file()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        return {"response": "no token"}
    response = await inquire_price(token_data["access_token"], '005930')
    print(response)
    return JSONResponse(content=response.json(), media_type="application/json; charset=UTF-8")





@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return {"item_name": item.name, "item_id": item_id, **item.model_dump()}


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


# 쿼리 매개변수
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# 기본값을 non으로 설정하여 선택적 매개변수를 선언
@app.get("/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
