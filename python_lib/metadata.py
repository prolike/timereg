from python_lib import shared, timestore
from datetime import datetime
from time import mktime as mktime
from collections import defaultdict
import sys
import os
import re
import logging


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
    chour = kwargs.get('chour', None)
    cminute = kwargs.get('cminute', None)
    format = time_format
    now = datetime.utcnow()
    if chour is not None:
        now = now.replace(hour=int(chour))
    if cminute is not None:
        now = now.replace(minute=int(cminute))
    return now.strftime(format)

def log(state, **kwargs):
    '''
    Makes our meta data string, that we are gonna use for logging time in git notes.

    Args:
        param1(str): state - if you 'start' the time log or 'end' it
        param2(str): chour - custom hour for the time returned
        param3(str): cminute - custom minute for the time returned

    Return:
        str: Returns a string with meta data including, git username, state (start or end),
        and timestamp with date (from the time method)
    '''
    logging.debug('Calling: shared.get_git_variables() to get username')
    username = shared.get_git_variables()['username']
    note_string = '[' + username + '][' + state + ']'
    value = kwargs.get('value', None)
    logging.debug('Calling: check_correct_order()')
    if check_correct_order(username, state) is True:
        try:
            if re.search(r'([01]\d|2[0-3]):[0-5]\d', value):
                chour = value.split(':')[0]
                cminute = value.split(':')[1]
                note_string += time(chour=chour, cminute=cminute)
                logging.debug('Calling: timestore.writetofile() to tempstore times')
                timestore.writetofile([note_string])
            elif re.search(r'([01]\d|2[0-3])?[0-5]\d', value):
                if len(value) is 3:
                    note_string += time(cminute=value[-2:], chour=value[:1])
                else:
                    note_string += time(cminute=value[-2:], chour=value[:2])
                logging.debug('Calling: timestore.writetofile() to tempstore times')
                timestore.writetofile([note_string])
        except:
            note_string += time()
            logging.debug('Calling: timestore.writetofile() to tempstore times')
            timestore.writetofile([note_string])
    else:
        try:
            s = re.search(r'((\d{2}-){2}(\d{4}))/(([01]\d|2[0-3]):[0-5]\d)', \
                          ''.join(timestore.readfromfile()[-1:]))
            print('You already', state + 'ed your timer!', s.group(0))
            return False
        except:
            print('You already', state + 'ed your timer!', ''.join(timestore.readfromfile()[-1:]))
            return False
    return True

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
    logging.debug('Calling: timestore.readfromfile() to get tempdata from file')
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
        if metadata[1] == 'end' and state == 'start' or last_value is -1:
            return True
        elif metadata[1] == 'start' and state == 'end':
            return True
    except:
        if last_value is -1 and state == 'start':
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
    fmt = '%d-%m-%Y/%H:%M'
    total_min_worked = 0

    logging.debug('Calling: timestore.writetofile() to tempstore times')
    name = get_clean_name_meta_data(started)
    logging.debug('Calling: timestore.writetofile() to tempstore times')
    clean_start = get_clean_time_meta_data(started)
    logging.debug('Calling: timestore.writetofile() to tempstore times')
    clean_end = get_clean_time_meta_data(ended)
    
    logging.debug('Checking for missing timestamps')
    if len(started) > len(ended):
        logging.warning('You are missing some timestamps!')
    logging.debug('Calculating time worked')
    for start_time, end_time in zip(clean_start, clean_end):
        d1 = mktime(datetime.strptime(start_time, fmt).timetuple())
        d2 = mktime(datetime.strptime(end_time, fmt).timetuple())
        total_min_worked += (int(d2-d1) / 60) #Prints time worken in min
    return total_min_worked

def get_clean_time_meta_data(meta_data):
    '''
    Seperating the good metadata timewise and the bad metadata timewise

    Args:
        param1(list): meta_data - A list containing metadata that needs cleaning

    Return:
        list: Returns a list of only valid timestamps
    '''
    cleaned_data = []
    for data in meta_data:
        cleaned_data.append(re.search(r'((\d{2}-){2}(\d{4}))/(([01]\d|2[0-3]):[0-5]\d)', \
                            data).group(0)) #Very brittle!
    return cleaned_data

def get_clean_name_meta_data(meta_data):
    '''
    Seperating username from rest of the metadata

    Args:
        param1(list): meta_data - A list containing metadata that needs username pulled out

    Return:
        str: Returns a string of the username supplied in the meta_data
    '''
    return re.findall(r'\[(.+?)\]', meta_data[0])[0]

def clean_meta_list(dirtylist):
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
        date = re.search(r'((\d{2}-){2}(\d{4}))/(([01]\d|2[0-3]):[0-5]\d)', data_element).group(0)
        datetime.strptime(date, format)
    except:
        return True
    return False

def check_all_closed(time_list):
    time_list = clean_meta_list(time_list)
    start, end = timestore.listsplitter(time_list)
    if len(start) is len(end):
        return True
    else:
        return False

def get_date(string):
    return re.search(r'((\d{2}-){2}(\d{4}))', string).group(0)

def split_on_days(time_list):
    diff_days = defaultdict(list)
    for each1 in time_list:
        diff_days[get_date(each1)].append(each1)  
    return diff_days