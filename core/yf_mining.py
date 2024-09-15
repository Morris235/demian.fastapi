import yfinance as yf
import pandas as pd

tickers = ['005930', '010145', '010050']

def get_stock_price_data(tickers: list[str], start: str, end: str):
    meta = yf.download(tickers, start=start, end=end)
    print(meta)