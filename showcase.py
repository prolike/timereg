from datetime import datetime, timedelta
from tzlocal import get_localzone
import arrow, pytz, timeit


def time_datetime():
    local_tz = get_localzone()
    tz = pytz.timezone(str(local_tz))
    tz_offset = datetime.now(pytz.timezone(str(local_tz))).strftime('%z')
    hour = tz_offset[0:1] + tz_offset[1:3]
    minut = tz_offset[0:1] + tz_offset[3:5]
    td = timedelta(hours=int(hour), minutes=int(minut))
    now = datetime.utcnow() + td
    now = tz.localize(now)
    return now.strftime('%Y-%m-%dT%H:%M:%S%z')

def time_arrow():
    utc = arrow.utcnow()
    print(utc)
    local = utc.to(str(get_localzone()))
    return local.format('YYYY-MM-DDTHH:mm:ssZ')
    
dts = time_datetime()
ars = time_arrow()
print(ars)

def arrow_parse(ars):
    return arrow.get(ars, 'YYYY-MM-DDTHH:mm:ssZ')
    
def datetime_parse(dts):
    tz = dts[-5:]
    timeObj = datetime.strptime(dts[:-5], '%Y-%m-%dT%H:%M:%S')
    return timeObj, tz

# print('Arrow make', timeit.timeit('time_arrow()', setup='from __main__ import arrow, get_localzone, time_arrow', number=100000))
# print('datetime make', timeit.timeit('time_datetime()', setup='from __main__ import datetime, timedelta, get_localzone, pytz, time_datetime', number=100000))

# print('arrow parse', timeit.timeit('arrow_parse(ars)', setup='from __main__ import arrow, arrow_parse, ars', number=100000))
# print('datetime parse', timeit.timeit('datetime_parse(dts)', setup='from __main__ import datetime, datetime_parse, dts', number=100000))