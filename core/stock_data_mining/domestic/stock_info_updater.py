import asyncio
from typing import Awaitable
from datetime import datetime, timedelta
from pandas.core.interchange.dataframe_protocol import DataFrame
import yfinance as yf
from core.core_env import krx_markets, stock_data_interval
from operations.redis_operations import redis_client
from utils.time_utils import get_current_business_days

def stock_price_update(interval: stock_data_interval = stock_data_interval.FIFTEEN_MIN):
    business_days : list[str] = business_last_days(interval)
    print(business_days)
    for market in krx_markets:
        hash_data: Awaitable[dict] | dict = redis_client.hgetall("stock_code_"+market.lower())
        decode_data: dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data.items()}
        for key in decode_data.keys():
            data_frame: DataFrame = yf.download(key + '.KS', start=business_days[0], end=business_days[-1], interval=interval.value)
            print(f'update stock info {market} : {key}')
            print(f"{data_frame}")

# FIXME: 1분 단위의 경우 영업일 기준 7일의 데이터를 가져오려고 했으나, yfinance.download의 내부에서 start, end 기준으로 7일을 계산한다.
# FIXME: ex) 2024-09-13 - 2024-09-20 = 7. 내부에서 이런식으로 계산한다. 하지만 저 기간은 추석이 끼여 있었기 때문에 3일치의 데이터 밖에 없다.
# 1분 단위 주가는 한번 요청에 7일간의 데이터만 가져올수 있다.
# 15분 단위 주가는 한번 요청에 60일간의 데이터만 가져올수 있다.
# 1시간 단위 주가는 한번 요청에 730일간의 데이터만 가져올수 있다.
def business_last_days(interval: stock_data_interval, year: int = datetime.now().year, month: int = datetime.now().month) -> list[str]:
    match interval:
        case interval.ONE_MIN:
            return get_current_business_days(year, month)[-7:]
        case interval.FIFTEEN_MIN:
            return get_current_business_days(year, month)[-60:]
        case interval.HOUR:
            return get_current_business_days(year, month)[-730:]
        case interval.DAY:
            return get_current_business_days(year, month)

async def main():
    try:
        stock_price_update()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception {e}")