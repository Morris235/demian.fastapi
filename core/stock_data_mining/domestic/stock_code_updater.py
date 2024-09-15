import asyncio
import FinanceDataReader as fdr
import pandas as pd
import time

from core.redis_config import redis_config

# KRX stock symbol list
stocks = fdr.StockListing('KRX')  # 코스피, 코스닥, 코넥스 전체
# stocks = fdr.StockListing('KOSPI') # 코스피
# stocks = fdr.StockListing('KOSDAQ') # 코스닥
# stocks = fdr.StockListing('KONEX') # 코넥스

rd = redis_config()

def update_code():
    timestamp = time.time()
    stocks_subset = stocks[['Code', 'Name']]
    stock_data_dict = {'timestamp':timestamp}
    hash_key = 'stock_data'

    for _, row in stocks_subset.iterrows():
        stock_code = row['Code']
        stock_name = row['Name']
        stock_data_dict[stock_code] = stock_name

    for key, value in stock_data_dict.items():
        rd.hset(hash_key, key, value)
    ##
    # {
    #   'timestamp' : '1630885400',
    #   '005930' :  '삼성전자'
    # }
    #
    # #

async def main():
    try:
        update_code()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception {e}")