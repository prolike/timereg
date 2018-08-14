from python_lib import shared
from datetime import datetime
from time import mktime as mktime
import sys
import os
import re
import webbrowser
import subprocess
import logging


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
    format = "%d-%m-%Y/%H:%M"
    now = datetime.now()
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
    note_string = '[' + shared.get_git_variables()['username'] + '][' + state + ']'
    value = kwargs.get('value', None)
    try:
        if re.search(r"([01]\d|2[0-3]):[0-5]\d", value):
            chour = value.split(":")[0]
            cminute = value.split(":")[1]
            note_string += time(chour=chour, cminute=cminute)
            print(note_string)
        elif re.search(r"([01]\d|2[0-3])?[0-5]\d", value):
            if len(value) is 3:
                note_string += time(cminute=value[-2:], chour=value[:1])
            else:
                note_string += time(cminute=value[-2:], chour=value[:2])
            print(note_string)
        else:
            note_string += time()
            print(note_string)
    except:
        note_string += time()
        print(note_string)
    return 1

def calc_time_worked(started, ended):
    '''
    Calculates the time spent working from the metadata in the git notes

    Args:
        param1(list): Started - A list containing metadata with the tag started
        param2(list): ended - A list containing metadata with the tag ended

    Return:
        str: Returns a string with amount of minutes worked with the provided information
    '''
    fmt = "%d-%m-%Y/%H:%M"
    total_min_worked = 0

    logging.debug('Cleaning metadata')
    name = get_clean_name_meta_data(started)
    clean_start = get_clean_time_meta_data(started)
    clean_end = get_clean_time_meta_data(ended)
    
    #print(name, clean_start, clean_end)
    logging.debug("Checking for missing timestamps")
    if len(started) > len(ended):
        logging.warning("You are missing some timestamps!")
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
        cleaned_data.append(re.search(r'((\d{2}-){2}(\d{4}))/(([01]\d|2[0-3]):[0-5]\d)', data).group(0)) #Very brittle!
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
    format = "%d-%m-%Y/%H:%M"
    metatag = re.findall(r'\[(.*?)\]', data_element)
    try:
        if metatag[1] != "start" and metatag[1] != "end":
            return True
        if len(metatag[0]) == 0 or len(metatag[0]) > 39:
            return True    
        date = re.search(r'((\d{2}-){2}(\d{4}))/(([01]\d|2[0-3]):[0-5]\d)', data_element).group(0)
        datetime.strptime(date, format)
    except:
        return True
    return False