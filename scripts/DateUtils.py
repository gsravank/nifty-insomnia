from datetime import datetime
from datetime import timedelta
import calendar

# https://www1.nseindia.com/global/content/market_timings_holidays/market_timings_holidays.htm

Holidays_exchange = ()


def get_dates_of_weekday(year, month, weekday_name='thursday'):
    """Get all dates in given month which fall on the given weekday
    
    Args:
        year (str): Year in YYYY format
        month (str): Month in MM format
        weekday_name (str): One of the seven weekday names
    
    Returns:
        list : List of dates matching given weekday
    """
    year = str(year)
    month = f"{int(month):02d}"
    
    date = f"{year}{month}01"
    weekday_name = weekday_name.strip().lower()
    weekdays = list()
    
    done = False
    while not done:
        if get_weekday_name(date).lower().strip() == weekday_name:
            weekdays.append(date)
        
        date = get_next_date(date)
        if date[4:6] != month:
            done = True
            
    return weekdays


def get_nsefo_monthly_expiry_date(date, holidays=Holidays_exchange):
    """Get monthly expiry date for an NSEFO contract of given date
    
    Args:
        date (str): Date in YYYYMMDD format
        holidays (list): List of holidays to ignore
        
    Returns:
        str : Expiry date in YYYYMMDD format
    """
    last_thursday = get_dates_of_weekday(date[:4], date[4:6], 'thursday')[-1]
    
    if date > last_thursday:
        curr_month_num = int(date[4:6])
        curr_year = int(date[:4])
        
        if curr_month_num == 12:
            next_month_num = 1
            next_year_num = curr_year + 1
        else:
            next_month_num = curr_month_num + 1
            next_year_num = curr_year
        next_month = f"{next_month_num:02d}"
        next_year = f"{next_year_num}"

        last_thursday = get_dates_of_weekday(next_year, next_month, 'thursday')[-1]
    
    if last_thursday in holidays:
        return get_prev_working_day(last_thursday, holidays)
    else:
        return last_thursday


def get_nsefo_prev_monthly_expiry_date(date, holidays=Holidays_exchange):
    """Get prev monthly expiry date for an NSEFO contract of given date
    
    Args:
        date (str): Date in YYYYMMDD format
        holidays (list): List of holidays to ignore
        
    Returns:
        str : Expiry date in YYYYMMDD format
    """
    curr_monthly_expiry_date = get_nsefo_monthly_expiry_date(date, holidays)
    curr_date = curr_monthly_expiry_date
    count = 0
    while True:
        count += 1
        prev_working_date = get_prev_working_day(curr_date)
        if curr_monthly_expiry_date != get_nsefo_monthly_expiry_date(prev_working_date, holidays):
            return get_nsefo_monthly_expiry_date(prev_working_date, holidays)
        else:
            curr_date = prev_working_date
        
        if count >= 60:
            print("Could not find prev monthly expiry!")
            return None
            
    return

    
def get_nsefo_weekly_expiry_date(date, holidays=Holidays_exchange):
    """Get weekly expiry date for an NSEFO contract of given date
    
    Args:
        date (str): Date in YYYYMMDD format
        holidays (list): List of holidays to ignore
        
    Returns:
        str : Expiry date in YYYYMMDD format
    """
    next_thursdays = [x for x in get_dates_of_weekday(date[:4], date[4:6], 'thursday') if x >= date]
    
    if len(next_thursdays) == 0:
        curr_month_num = int(date[4:6])
        curr_year = int(date[:4])
        
        if curr_month_num == 12:
            next_month_num = 1
            next_year_num = curr_year + 1
        else:
            next_month_num = curr_month_num + 1
            next_year_num = curr_year
        next_month = f"{next_month_num:02d}"
        next_year = f"{next_year_num}"
        
        next_thursday = get_dates_of_weekday(next_year, next_month, 'thursday')[0]
    else:
        next_thursday = next_thursdays[0]

    if next_thursday in holidays:
        return get_prev_working_day(next_thursday, holidays)
    else:
        return next_thursday


def get_todays_date():
    return datetime.today().strftime("%Y%m%d")


def get_prev_date(date):
    dt = datetime.strptime(date, "%Y%m%d")
    prev_dt = dt - timedelta(days=1)
    return prev_dt.strftime("%Y%m%d")


def get_next_date(date):
    dt = datetime.strptime(date, "%Y%m%d")
    next_dt = dt + timedelta(days=1)
    return next_dt.strftime("%Y%m%d")


def get_weekday_name(date):
    return calendar.day_name[datetime.strptime(date, "%Y%m%d").weekday()]


def get_next_working_day( date, holidays=Holidays_exchange):
    next_day = datetime.strptime(date, "%Y%m%d")
    while True:
        next_day += timedelta(days=1)
        if next_day.weekday() >= 5:
            continue
        if next_day.strftime("%Y%m%d") in holidays:
            continue
        return next_day.strftime("%Y%m%d")


def get_prev_working_day( date, holidays=Holidays_exchange):
    prev_day = datetime.strptime(date, "%Y%m%d")
    while True:
        prev_day -= timedelta(days=1)
        if prev_day.weekday() >= 5:
            continue
        if prev_day.strftime("%Y%m%d") in holidays:
            continue
        return prev_day.strftime("%Y%m%d")
    return "-1"


def convert_date_to_bhav_style(date):
    """Convert date from YYYYMMDD to DD-MMM-YYYY format
    Example: 20210624 -> 24-Jun-2021
    """
    month = calendar.month_name[int(date[4:6])][:3].title()
    return f"{date[6:]}-{month}-{date[:4]}"


def get_working_days(start_date, end_date, num_days, exchange, weekday=""):
    holidays = Holidays_exchange
    days = []
    if start_date != "-1" and end_date != "-1":
        start_date = get_prev_working_day(start_date, holidays)
        end_date = get_next_working_day(end_date, holidays)
        end_date = get_prev_working_day(end_date, holidays)
        while start_date != end_date:
            start_date = get_next_working_day(start_date, holidays)
            days.append(start_date)
    if start_date != "-1" and num_days != "-1":
        start_date = get_prev_working_day(start_date, holidays)
        for num in range(int(num_days)):
            start_date = get_next_working_day(start_date, holidays)
            days.append(start_date)
    if end_date != "-1" and num_days != "-1":
        end_date = get_next_working_day(end_date, holidays)
        for num in range(int(num_days)):
            end_date = get_prev_working_day(end_date, holidays)
            days.insert(0, end_date)

    if weekday == "":
        return days
    else:
        return [day for day in days if get_weekday_name(day).lower() == weekday.strip().lower()]
