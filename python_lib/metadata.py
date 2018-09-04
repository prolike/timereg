from python_lib import shared, timestore
from datetime import datetime
from time import mktime as mktime
from collections import defaultdict
from tzlocal import get_localzone
import datetime as dt
import sys, os, re, logging, pytz


time_format = shared.get_time_format()

def time(**kwargs):
    logging.debug(f'Calling: metadata.time({kwargs})')
    '''
    Makes custom time format with date, and possibility of using,
    custom hour and minute

    Args:
        param1(str): chour - custom hour for the time returned
        param2(str): cminute - custom minute for the time returned

    Return:
        str: Returns a string of the current time or custom time with the current date
    '''
    chour = kwargs.get('chour', None)
    cminute = kwargs.get('cminute', None)
    cday = kwargs.get('cday', None)
    cmonth = kwargs.get('cmonth', None)
    local_tz = get_localzone()
    #print(f'local_tz, {local_tz}')
    tz = pytz.timezone(str(local_tz))
    #print(f'tz, {tz}')
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

def check_correct_order(username, state):
    logging.debug(f'Calling: metadata.check_correct_order({username}, {state})')
    '''
    Checks if the user already has a 'open' time log or open 'end' log
    and makes sure they dont double open or double closes

    Args:
        param1(str): username - the username of the user working on the current issue
        param2(str): state - if the user wanna start or end time logging

    Return:
        bool: true or false depending on the criterias
    '''
    data_list = timestore.readfromfile()
    last_value = -1
    for idx, element in enumerate(data_list):
        metadata = re.findall(r'\[(.*?)\]', element)
        if metadata[0] == username:
            last_value = idx
    try:
        metadata = re.findall(r'\[(.*?)\]', data_list[last_value])
    except:
        pass
    try:
        if metadata[1] == 'end' and state == 'start' or metadata[1] == 'end' and state == 'did' or last_value is -1:
            return True
        elif metadata[1] == 'start' and state == 'end':
            return True
    except:
        if last_value is -1 and state == 'start':
            return True   
    return False


def calc_time_worked(started, ended):
    logging.debug(f'Calling: metadata.calc_time_worked({started}, {ended})')
    '''
    Calculates the time spent working from the metadata in the git notes

    Args:
        param1(list): Started - A list containing metadata with the tag started
        param2(list): ended - A list containing metadata with the tag ended

    Return:
        str: Returns a string with amount of minutes worked with the provided information
    '''
    fmt = time_format
    sec_worked = 0

    #name = get_clean_name_meta_data(started)
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
    logging.debug(f'Calling: metadata.get_clean_time_meta_data({meta_data})')
    '''
    Seperating the good metadata timewise and the bad metadata timewise

    Args:
        param1(list): meta_data - A list containing metadata that needs cleaning

    Return:
        list: Returns a list of only valid timestamps
    '''
    cleaned_data = []
    for data in meta_data:
        cleaned_data.append(re.search(r'(\d{4}(-\d{2}){2})T(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', \
                            data).group(0)) #Very brittle!
    return cleaned_data

def get_clean_name_meta_data(meta_data):
    logging.debug(f'Calling: metadata.get_clean_name_meta_data({meta_data})')
    '''
    Seperating username from rest of the metadata

    Args:
        param1(list): meta_data - A list containing metadata that needs username pulled out

    Return:
        str: Returns a string of the username supplied in the meta_data
    '''
    return re.findall(r'\[(.+?)\]', meta_data[0])[0]

def clean_meta_list(dirtylist):
    logging.debug(f'Calling: metadata.clean_meta_list({dirtylist})')
    '''
    Seperating the good metadata timewise and the bad metadata timewise

    Args:
        param1(list): dirtylist - A list containing metadata that needs cleaning

    Return:
        list: Returns a list of only valid timestamps
    '''
    index_remove = []
    clean_list = dirtylist
    for idx, element in enumerate(dirtylist):
        if cleaner(element) is True:
            index_remove.append(idx)
    index_remove.reverse()
    for idx in index_remove:
        del clean_list[idx]
    return clean_list

def cleaner(data_element):  
    logging.debug(f'Calling: metadata.cleaner({data_element})')  
    '''
    Making sure all the data in the data_element is valid, and telling if the provided
    string should be allowed to continue or deleted

    Args:
        param1(list): data_element - A string containing metadata that needs username pulled out

    Return:
        bool: Returns True or False depending on how the test goes
    '''
    format = time_format
    metatag = re.findall(r'\[(.*?)\]', data_element)
    try:
        if metatag[1] != 'start' and metatag[1] != 'end':
            return True
        if len(metatag[0]) == 0 or len(metatag[0]) > 39:
            return True    
        date = re.search(r'(\d{4}(-\d{2}){2})T(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', data_element).group(0)
        datetime.strptime(date, format)
    except:
        return True
    return False

def check_all_closed(time_list):
    logging.debug(f'Calling: metadata.check_all_closed({time_list})')
    time_list = clean_meta_list(time_list)
    start, end = timestore.listsplitter(time_list)
    if len(start) is len(end):
        return True
    else:
        return False

def get_date(value):
    logging.debug(f'Calling: metadata.get_date({value}))')
    if type(value) is str:
        return re.search(r'(\d{4}(-\d{2}){2})', value).group(0)
    elif type(value) is list:
        res = []
        for each in value:
            res.append(re.search(r'(\d{4}(-\d{2}){2})', each).group(0))
        return res


def split_on_days(time_list):
    logging.debug(f'Calling: metadata.split_on_days({time_list})')
    time_list = order_days(time_list)
    diff_days = defaultdict(list)
    d_list = get_date(time_list)
    for each, each_date in zip(time_list, d_list):
        diff_days[each_date].append(each)  
    return diff_days

def order_days(value): #TODO Make single extract call!
    logging.debug(f'Calling: metadata.order_days({value})')
    dates2 = extract_timestamp(value)
    dates = value
    dates2.sort(key=lambda date: datetime.strptime(date[:-5], '%Y-%m-%dT%H:%M:%S'))
    test_dates = []
    for each2 in dates2:
        for each in dates:
            if each2 in each:
                test_dates.append(each)
    return test_dates

def extract_time(value):
    logging.debug(f'Calling: metadata.extract_time({value})')
    if type(value) is str:
        return re.search(r'(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', value).group(0)
    elif type(value) is list:
        res = []
        for each in value:
            res.append(re.search(r'(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', each).group(0))
        return res

def extract_timestamp(value):
    logging.debug(f'Calling: metadata.extract_timestamp({value})')
    if type(value) is str:
        return re.search(r'(\d{4}(-\d{2}){2})T(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', value).group(0)
    elif type(value) is list:
        res = []
        for each in value:
            res.append(re.search(r'(\d{4}(-\d{2}){2})T(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', each).group(0))
        return res

def seconds_to_timestamp(value):
    logging.debug(f'Calling: metadata.seconds_to_timestamp({value})')
    return str(dt.timedelta(seconds=value))