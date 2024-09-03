from fastapi import APIRouter

from api.v1.local.inquiry import inquire_price
from utils.time_utils import second_today
from utils.token_handler import load_token_from_file

router: APIRouter = APIRouter()

@router.get("/inquire/price", tags=["inquire"])
async def response_inquire_price():
    token_data = load_token_from_file()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        return {"response": "no token"}
    response = await inquire_price(token_data["access_token"], '005930')
    print(response)
    return response