from datetime import datetime
from pytz import timezone

'''this function should be run in the morning of each game day
example url to create :  https://statsapi.web.nhl.com/api/v1/schedule?date=2021-11-24
'''
'''
takes a string type as date
'''
def api_url_maker(date):
    front = "https://statsapi.web.nhl.com/api/v1/schedule?date="
    today = date
    complete_url = front+today
    return complete_url

def todays_date():
    # define date format
    fmt = "%Y-%m-%d"
    # define eastern timezone
    eastern = timezone('US/Eastern')
    # naive datetime
    naive_dt = datetime.now()
    # localized datetime
    loc_dt = datetime.now(eastern)
    today = loc_dt.strftime(fmt)
    return today