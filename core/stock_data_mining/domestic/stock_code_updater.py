import asyncio
import FinanceDataReader as fdr
import time
from core.redis_config import redis_config
from core.core_env import krx_markets

rd = redis_config()

def krx_stock_code_update():
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

async def main():
    try:
        krx_stock_code_update()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception {e}")