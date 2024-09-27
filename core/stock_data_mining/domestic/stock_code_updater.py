import asyncio
from datetime import datetime as dt, timedelta, datetime
from typing import Awaitable
import yfinance as yf
import FinanceDataReader as fdr
import time
import pandas
from dateutil.relativedelta import relativedelta

from core.redis_config import redis_config
from core.core_env import krx_markets, StockDataInterval
from utils.time_utils import business_last_days

rd = redis_config()

# 매달 1일에 자동 실행
def stock_code_update():
    timestamp = time.time()
    stock_data_dict = {'timestamp':timestamp}
    hash_key = 'stock_code_'

    for market in krx_markets:
        stocks_dataframe = fdr.StockListing(market)
        stocks_subset = stocks_dataframe[['Code', 'Name']]
        for _, row in stocks_subset.iterrows():
            stock_code = row['Code']
            stock_name = row['Name']
            stock_data_dict[stock_code] = stock_name
            for key, value in stock_data_dict.items():
                print(f"update stock code {market} : {key}")
                rd.hset(hash_key+market.lower(), key, value)

def get_last_month_date():
    today = datetime.today()
    last_month_first = datetime(today.year, today.month, 1) + relativedelta(month=1)
    return last_month_first.strftime("%Y-%m-%d")

# 매달 1일에 자동 실행 : 조건에 부합하는 전 달의 모든 주가종목을 update한다.
def target_stock_code_update(interval: StockDataInterval = StockDataInterval.DAY, base_vol: int = 500000):
    try:
        now = dt.now()
        month = now.date().month

        business_days : list[str] = business_last_days(interval, month=month)
        print(business_days)
        for market in krx_markets:
            hash_data: Awaitable[dict] | dict = rd.hgetall("stock_code_"+market.lower())
            decode_data: dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data.items()}

            for field, value in decode_data.items():
                yf_df: pandas.DataFrame = yf.download(field + '.KS', start=business_days[0], end=business_days[-1], interval=interval.value)
                yf_df.reset_index(inplace=True)

                avg_vol = yf_df["Volume"].mean()

                if avg_vol >= base_vol:
                    print(f'market : {market}, stock : ({field}) {value}, avg_vol : {avg_vol}, interval : {interval.value}')
                    rd.hset(f"target_stock_code_kospi:{now.date()}", field, value)

    except Exception as e:
        print(e)

async def main():
    try:
        # stock_code_update()
        target_stock_code_update()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception {e}")