from core.redis_config import redis_config
import gzip
import json
from datetime import datetime as dt

rd = redis_config()

def get_all_target_stock_price():
    hash_data = rd.hgetall(f"target_stock_price_kospi:{dt.now().date()}")

    for key, compressed_data in hash_data.items():
        try:
            decompressed_data = gzip.decompress(compressed_data)

            stock_list = json.loads(decompressed_data.decode(
                'utf-8'))

            print(stock_list)
        except Exception as e:
            print(e)

def get_target_stock_price(stock_code: str = "005930"):
    hash_data = rd.hget(f"target_stock_price_kospi:{dt.now().date()}",key=stock_code)

    try:
        decompressed_data = gzip.decompress(hash_data)
        stock_list: list = json.loads(decompressed_data.decode(
            'utf-8'))
        print(stock_list[-1].get("open"))

    except Exception as e:
        print(e)