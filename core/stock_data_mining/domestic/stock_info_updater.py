import asyncio
from typing import Awaitable
import yfinance as yf
from operations.redis_operations import redis_client


# 1분 단위 주가는 7일간의 데이터만 가져올수 있다.
# 15분 단위 주가는 60일간의 데이터만 가져올수 있다.
# 1시간 단위 주가는 730일간의 데이터만 가져올수 있다.
def stock_price_update():
    hash_data: Awaitable[dict] | dict = redis_client.hgetall("stock_code_krx")
    decode_data: dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data.items()}

    for key in decode_data.keys():
        data_frame = yf.download(key + '.KS', start="2024-08-01", end="2024-09-01", interval="15m")
        print(data_frame)


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