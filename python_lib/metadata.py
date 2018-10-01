from python_lib import shared, git_timestore_calls as gtc
from datetime import datetime
from time import mktime as mktime
from collections import defaultdict
from tzlocal import get_localzone
import datetime as dt
import sys
import os
import re
import logging
import pytz


time_format = shared.get_time_format()


def time(**kwargs):
    '''
    Makes custom time format with date, and possibility of using,
    custom hour and minute

    Args:
        param1(str): chour - custom hour for the time returned
        param2(str): cminute - custom minute for the time returned

    Return:
        str: Returns a string of the current time or custom time with the current date
    '''
    logging.debug(f'metadata.time({kwargs})')
    chour = kwargs.get('chour', None)
    cminute = kwargs.get('cminute', None)
    cday = kwargs.get('cday', None)
    cmonth = kwargs.get('cmonth', None)
    local_tz = get_localzone()
    # print(f'local_tz, {local_tz}')
    tz = pytz.timezone(str(local_tz))
    # print(f'tz, {tz}')
    format = time_format
    now = datetime.utcnow()
    now = tz.localize(now)
    if chour is not None:
        now = now.replace(hour=int(chour))
    if cminute is not None:
        now = now.replace(minute=int(cminute))
    if cday is not None:
        now = now.replace(day=int(cday))
    if cmonth is not None:
        now = now.replace(month=int(cmonth))
    return now.strftime(format)

def get_tz_info():
    format = time_format    
    local_tz = get_localzone()
    tz = pytz.timezone(str(local_tz))
    now = datetime.utcnow()
    now = tz.localize(now)
    return now.strftime(format)[-5:]

def check_correct_order(username, state):
    '''
    Checks if the user already has a 'open' time log or open 'end' log
    and makes sure they dont double open or double closes

    Args:
        param1(str): username - the username of the user working on the current issue
        param2(str): state - if the user wanna start or end time logging

    Return:
        bool: true or false depending on the criterias
    '''
    logging.debug(f'metadata.check_correct_order({username}, {state})')
    test = gtc.get_all_as_dict()
    data_list = order_days(test)
    last_value = -1
    for idx, element in enumerate(data_list):
        if element['user'] == username:
            last_value = idx
    try:
        cstate = data_list[last_value]['state']
        if cstate == 'end' and state == 'start' or cstate == 'end' and state == 'did' or cstate == 'start' and state == 'end' or last_value is -1:
            return True
    except:
        if last_value is -1 and state == 'start' or last_value is -1 and state == 'did':
            return True 
    return False

def calc_time_worked(started, ended):
    '''
    Calculates the time spent working from the metadata in the git notes

    Args:
        param1(list): Started - A list containing metadata with the tag started
        param2(list): ended - A list containing metadata with the tag ended

    Return:
        str: Returns a string with amount of minutes worked with the provided information
    '''
    logging.debug(f'metadata.calc_time_worked({started}, {ended})')
    # print(started)
    fmt = time_format
    sec_worked = 0

    # name = get_clean_name_meta_data(started)
    clean_start = get_clean_time_meta_data(started)
    clean_end = get_clean_time_meta_data(ended)

    if len(started) > len(ended):
        logging.warning('You are missing some timestamps!')
    for start_time, end_time in zip(clean_start, clean_end):
        d1 = mktime(datetime.strptime(start_time, fmt).timetuple())
        d2 = mktime(datetime.strptime(end_time, fmt).timetuple())
        sec_worked += (int(d2-d1))
    return sec_worked

def get_clean_time_meta_data(meta_data):
    '''
    Seperating the good metadata timewise and the bad metadata timewise

    Args:
        param1(list): meta_data - A list containing metadata that needs cleaning

    Return:
        list: Returns a list of only valid timestamps
    '''
    logging.debug(f'metadata.get_clean_time_meta_data({meta_data})')
    cleaned_data = []
    if type(meta_data) is list:
        for data in meta_data:
            if type(data) is dict:
                cleaned_data.append(data['timestamp'])
    return cleaned_data

def get_date(value):
    logging.debug(f'metadata.get_date({value}))')
    if type(value) is list:
        res = []
        for each in value:
            res.append(re.search(r'(\d{4}(-\d{2}){2})', each['timestamp']).group(0))
        return res

def get_type(value):
    logging.debug(f'metadata.get_type({value}))')
    if type(value) is dict:
        return value['state']

def split_on_days(time_list):
    logging.debug(f'metadata.split_on_days({time_list})')
    time_list = order_days(time_list)
    diff_days = defaultdict(list)
    d_list = get_date(time_list)
    earlier_day = ''
    for each, each_date in zip(time_list, d_list):
        if get_type(each) == 'end':
            diff_days[earlier_day].append(each)
        else:
            diff_days[each_date].append(each)
            earlier_day = each_date
    return diff_days

# def match_month(value, month):
#     if month == 'this':
#         month = datetime.utcnow().strftime('%m')
#         print(type(month))
#     res = []
#     for each in value:
#         try:
#             re.search(r'(\d{4}(-(' + month + r'))(-\d{2}))', each).group(0)
#             res.append(each)
#         except:
#             pass
#     return res

def match_week(value, week):
    res = []
    if week == 'this':
        week = datetime.utcnow().isocalendar()[1]
    for _, item in value.items():
            for _, content in item.items():
                res.append(content)
    return res

def order_days(value):  # TODO Make single extract call!
    logging.debug(f'metadata.order_days({value})')
    dates2 = extract_timestamp(value)
    dates = value
    dates2.sort(key=lambda date: datetime.strptime(
        date[:-5], '%Y-%m-%dT%H:%M:%S'))
    test_dates = []
    
    for each2 in dates2:
        for key1, item in dates.items():
            for key2, content in item.items():
                if each2 in content['timestamp']:
                    temp = content
                    temp['storage'] = {'issuehash': key1, 'linehash': key2}
                    test_dates.append(temp)
    return test_dates

def extract_time(value):
    logging.debug(f'metadata.extract_time({value})')
    if type(value) is list:
        res = []
        for each in value:
            res.append(
                re.search(r'(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', each['timestamp']).group(0))
        return res
    if type(value) is str:
        return re.search(r'(([01]\d|2[0-3])(:[0-5]\d))((:[0-5]\d)\+(\d{4}))?', value).group(0)

def extract_timestamp(value):
    logging.debug(f'metadata.extract_timestamp({value})')
    res = []
    if type(value) is dict:
        for _, item in value.items():
            for _, content in item.items():
                res.append(content['timestamp'])
    if type(value) is list:
        for each in value:
            res.append(each['timestamp'])
    return res

def seconds_to_timestamp(value):
    logging.debug(f'metadata.seconds_to_timestamp({value})')
    return str(dt.timedelta(seconds=value))
