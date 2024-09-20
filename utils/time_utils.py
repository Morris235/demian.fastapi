from datetime import datetime, timedelta
from pykrx import stock

def second_today() -> float:
    now = datetime.now()
    start_of_data = datetime(now.year, now.month, now.day)
    end_of_day = start_of_data + timedelta(days=1) - timedelta(seconds=1)
    return (end_of_day - start_of_data).total_seconds()

def get_current_business_days(year : int, month : int) -> list[str] :
    business_datetime : list[datetime] = stock.get_previous_business_days(year=year, month=month)
    business_days : list[str] = []
    for day in business_datetime:
        business_days.append(str(day).split(' ')[0])
    return business_days