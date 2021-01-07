import datetime, pytz

def get_datetime_now():
    tz = pytz.timezone('Asia/Bangkok')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S.%f')