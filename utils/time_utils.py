from datetime import datetime, timedelta
from pykrx import stock

from core.core_env import StockDataInterval

def today_to_sec() -> float:
    now = datetime.now()
    start_of_data = datetime(now.year, now.month, now.day)
    end_of_day = start_of_data + timedelta(days=1) - timedelta(seconds=1)
    return (end_of_day - start_of_data).total_seconds()

def get_current_business_days(year : int, month : int) -> list[str] :
    business_date : list[datetime] = stock.get_previous_business_days(year=year, month=month)
    business_days : list[str] = []
    for day in business_date:
        business_days.append(str(day).split(' ')[0])
    return business_days

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