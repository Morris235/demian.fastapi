from fastapi import APIRouter

from api.v1.local.order import order_stock
from utils.time_utils import second_today
from utils.token_handler import load_token_cache

router: APIRouter = APIRouter()

@router.get("/orders/stock", tags=["orders"])
async def response_inquire_price():
    token_data = load_token_cache()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        return {"response": "no token"}
    response = await order_stock(token_data["access_token"],'005930', '56200', '1')
    print(response)
    return response