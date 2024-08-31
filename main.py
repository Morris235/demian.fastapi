from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QObject, QEvent, QTimer, QCoreApplication

import sys
from main_window import Main_window
from balance_window import Balance_window

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.qt import QtScheduler

from dotenv import load_dotenv
import os

# load .env
load_dotenv()

loader = QUiLoader()

app = QApplication(sys.argv)

the_path = os.path.dirname(__file__)
os.environ['ROOT_FILE_PATH'] = the_path

SHUT_DOWN_FLAG = False

# 이 부분은 MacOS에서는 사용할 수 없으므로 주석 처리하거나 제거합니다.
# 이베스트 로그인 및 Windows 전용 부분은 삭제

# balance_window는 여전히 사용 가능
balance_window = Balance_window()

# 세션 및 로그인 로직 관련 부분 제거
# 대신, 다른 MacOS 관련 코드 또는 REST API 등을 사용할 수 있습니다.

window = Main_window()  # session과 balance_window는 필요하지 않습니다.
window.show()

# MacOS에서 사용하는 스케줄러는 유지됩니다.
scheduler = QtScheduler()

# 예시 작업 추가 (여기서는 5초마다 실행되는 간단한 작업을 추가)
def yeah():
    print('YEAH!!!!')

scheduler.add_job(yeah, 'interval', seconds=5)
scheduler.start()

# 메인 이벤트 루프 실행
app.exec_()


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
