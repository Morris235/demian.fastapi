import asyncio
import gzip
import json
from typing import Awaitable
from datetime import datetime
import pandas
import pandas as pd
import yfinance as yf
from matplotlib.font_manager import json_dump

from core.core_env import krx_markets, StockDataInterval
from core.redis_config import redis_config
from utils.time_utils import get_current_business_days

rd = redis_config()

def stock_price_update(interval: StockDataInterval = StockDataInterval.FIFTEEN_MIN):
    try:
        business_days : list[str] = business_last_days(interval)
        for market in krx_markets:
            hash_data: Awaitable[dict] | dict = rd.hgetall("stock_code_"+market.lower())
            decode_data: dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data.items()}
            for field, value in decode_data.items():
                yf_df: pandas.DataFrame = yf.download(field + '.KS', start=business_days[0], end=business_days[-1], interval=interval.value)
                yf_df.reset_index(inplace=True)

                avg_vol = yf_df["Volume"].mean()
                # print(avg_vol)
                if avg_vol >= 300000:
                    stock_list = []
                    print(f'market : {market}, stock : ({field}) {value}, avg_vol : {avg_vol}, interval : {interval.value}')
                    for index, row in yf_df.iterrows():
                        stock_dict = {
                            "dtime": row['Date'].strftime('%Y-%m-%d %H:%M:%S') if interval == StockDataInterval.DAY else row['Datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                            "open": row['Open'],
                            "high": row['High'],
                            "low": row['Low'],
                            "close": row['Close'],
                            "adj": row['Adj Close'],
                            "vol": row['Volume']
                        }
                        stock_list.append(stock_dict)
                    # compressed_data = gzip.compress(json.dumps(stock_list).encode('utf-8'))
                    rd.hset("stock_price_kospi", field, json.dumps(stock_list))
    except Exception as e:
        print(e)


# FIXME: 1분 단위의 경우 영업일 기준 7일의 데이터를 가져오려고 했으나, yfinance.download의 내부에서 start, end 기준으로 7일을 계산한다.
# FIXME: ex) 2024-09-13 - 2024-09-20 = 7. 내부에서 이런식으로 계산한다. 하지만 저 기간은 추석이 끼여 있었기 때문에 3일치의 데이터 밖에 없다.
# 1분 단위 주가는 한번 요청에 7일간의 데이터만 가져올수 있다.
# 15분 단위 주가는 한번 요청에 60일간의 데이터만 가져올수 있다.
# 1시간 단위 주가는 한번 요청에 730일간의 데이터만 가져올수 있다.
def business_last_days(interval: StockDataInterval, year: int = datetime.now().year, month: int = datetime.now().month) -> list[str]:
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
        # 전 종목 1 달간의 N시간 단위 주가 데이터 저장, (시장상황 분석[상승,하락])
        # 저장된 1 달간의 주가 데이터 기준,
        # 조건에(거래량, 상승/하락 폭, 체결 강도 등등. 이 부분은 어떤 종목의 조건이 데이트레이딩에 적합한지 공부 필요) 부합하는 종목에 대해서만 일주인간의 1분 단위 주가 정보 저장
        # -> 이 데이터를 기준으로 승률이 높은 종목을 분석
        stock_price_update(interval=StockDataInterval.DAY)
    except Exception as e:
         print(e)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception {e}")