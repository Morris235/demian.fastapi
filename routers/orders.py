from fastapi import APIRouter

from api.v1.domestic.order import order_stock
from utils.time_utils import today_to_sec
from utils.token_handler import load_token_cache

router: APIRouter = APIRouter()

@router.get("/orders/order/stock", tags=["orders"])
async def response_order_stock():
    token_data = load_token_cache()
    if token_data["access_token"] is None or token_data["expires_in"] < today_to_sec():
        return {"response": "no token"}
    response = await order_stock(token_data["access_token"],'005930', '56200', '1')
    print(response)
    return response
# {"rt_cd":"0","msg_cd":"40600000","msg1":"모의투자 매수주문이 완료 되었습니다.","output":{"KRX_FWDG_ORD_ORGNO":"00950","ODNO":"47589","ORD_TMD":"134354"}}