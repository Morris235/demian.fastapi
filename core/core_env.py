from enum import Enum

krx_markets = ['KOSPI', 'KOSDAQ']


class stock_data_interval(Enum):
    ONE_MIN = '1m'
    FIFTEEN_MIN = '15m'
    THIRTY_MIN = '30m'
    HOUR = '1h'
    DAY = '1d'
