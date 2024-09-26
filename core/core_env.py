from enum import Enum

krx_markets = ['KOSPI']
# krx_markets = ['KOSPI', 'KOSDAQ']
# krx_markets = ['KOSPI', 'KOSDAQ', 'KONEX']


class StockDataInterval(Enum):
    ONE_MIN = '1m'
    FIFTEEN_MIN = '15m'
    THIRTY_MIN = '30m'
    HOUR = '1h'
    DAY = '1d'
