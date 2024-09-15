from fastapi import APIRouter

from api.v1.domestic.inquire import inquire_price
from utils.time_utils import second_today
from utils.token_handler import load_token_cache

router: APIRouter = APIRouter()

@router.get("/inquires/price", tags=["inquires"])
async def response_inquire_price():
    token_data = load_token_cache()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        return {"response": "no token"}
    response = await inquire_price(token_data["access_token"], '005930')
    print(response)
    return response