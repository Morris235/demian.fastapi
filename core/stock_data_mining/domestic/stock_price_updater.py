import asyncio
import gzip
import json
from typing import Awaitable
from datetime import datetime as dt
import pandas
import yfinance as yf
from core.core_env import krx_markets, StockDataInterval
from core.redis_config import redis_config
from utils.time_utils import get_business_last_days, get_last_month_date

rd = redis_config()

def set_target_stock_price(interval: StockDataInterval = StockDataInterval.FIFTEEN_MIN):
    try:
        last_month = dt.now().month-1
        business_days : list[str] = get_business_last_days(interval, last_month)
        for market in krx_markets:
            hash_data: Awaitable[dict] | dict = rd.hgetall("target_stock_code_" + market.lower() +f":{get_last_month_date()}")
            decode_data: dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data.items()}
            for field, value in decode_data.items():
                yf_df: pandas.DataFrame = yf.download(field + '.KS', start=business_days[0], end=business_days[-1], interval=interval.value)
                yf_df.reset_index(inplace=True)

                stock_list = []
                print(f'market : {market}, stock : ({field}) {value}, interval : {interval.value}')
                for index, row in yf_df.iterrows():
                    stock_dict = {
                        "dtime": row['Date'].strftime('%Y-%m-%d %H:%M:%S') if interval == StockDataInterval.DAY else
                        row['Datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                        "open": row['Open'],
                        "high": row['High'],
                        "low": row['Low'],
                        "close": row['Close'],
                        "adj": row['Adj Close'],
                        "vol": row['Volume']
                    }
                    stock_list.append(stock_dict)
                compressed_data = gzip.compress(json.dumps(stock_list).encode('utf-8'))
                rd.hset(f"target_stock_price_kospi:{get_last_month_date()}", field, compressed_data)

    except Exception as e:
        print(e)

async def main():
    try:
        # 전 종목 1 달간의 N시간 단위 주가 데이터 저장, (시장상황 분석[상승,하락])
        # 저장된 1 달간의 주가 데이터 기준,
        # 조건에(거래량, 상승/하락 폭, 체결 강도 등등. 이 부분은 어떤 종목의 조건이 데이트레이딩에 적합한지 공부 필요) 거래량 30만 이상의 조건에 부합하는 종목에 대해서만 저장
        # -> 이 데이터를 기준으로 승률이 높은 종목을 분석
        set_target_stock_price()
    except Exception as e:
         print(e)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception {e}")