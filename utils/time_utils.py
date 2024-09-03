from datetime import datetime, timedelta

def second_today():
    now = datetime.now()
    start_of_data = datetime(now.year, now.month, now.day)
    end_of_day = start_of_data + timedelta(days=1) - timedelta(seconds=1)
    return (end_of_day - start_of_data).total_seconds()