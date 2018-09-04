from python_lib import shared, timestore, metadata
from datetime import datetime
import logging


time_format = shared.get_time_format()[:-2]

def test():
    print(check_booked_time(timestore.readfromfile(), metadata.time()))

def check_booked_time(t_list, value):
    logging.debug(f'Calling: dbook.check_booked_time({t_list}, {value})')
    date = metadata.get_date(value)
    d_list = get_list_of_day(t_list, date)
    start_date, end_date = timestore.listsplitter(d_list)
    for start, end in zip(start_date, end_date):
        start_sec = datetime.strptime(metadata.extract_timestamp(start)[:-5], time_format).timestamp()
        end_sec = datetime.strptime(metadata.extract_timestamp(end)[:-5], time_format).timestamp()
        val_sec = datetime.strptime(metadata.extract_timestamp(value)[:-5], time_format).timestamp()
        if checker(start_sec, end_sec, val_sec) is False:
            return False
    return True

def get_list_of_day(t_list, date):
    logging.debug(f'Calling: dbook.get_list_of_day({t_list}, {date})')
    o_list = []
    d_list = metadata.get_date(t_list)
    for each, each_date in zip(t_list, d_list):
        if each_date == date:
            o_list.append(each)
    return o_list

def checker(start, end, value):
    logging.debug(f'Calling: dbook.checker({start}, {end}, {value})')
    if start < value > end:
        pass
    else:
        return False