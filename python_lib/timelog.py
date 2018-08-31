from python_lib import shared, timestore, metadata
from datetime import datetime
import re, logging


time_format = shared.get_time_format()[:-2]

def log_type(state, **kwargs):
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
    username = shared.get_git_variables()['username']
    note_string = '[' + username + '][' + state + ']'
    value = kwargs.get('value', None)
    if metadata.check_correct_order(username, state) is True:
        try:
            return _state_types(state, value, note_string)
        except:
            _write_note(note_string, value)
    else:
        return _error(state)
    return True

def _state_types(state, value, note_string):
    if state == 'did':
        _did_test(value)
    elif state == 'end' or state == 'start':
        if _custom_check(value) is False:
            return False
        _write_note(note_string, value)
        return True

def _custom_check(value):
    if re.search(r'([01]\d|2[0-3])(:*)[0-5]\d', value):
        return True
    else:
        if re.search(r'([01]\d|2[0-3])(:*)\d', value):
            print('Seems like you forgot a digit!\nPlease use the following format: hh:mm or hhmm')
            return False
        else:
            return False

def _did_test(value):
    if re.search(r'((\d){1,2})([h]|[H])', value):
        value2 = re.search(r'((\d){1,2})([h]|[H])', value).group(0)
        test_time = metadata.time()[:-5]
        hour = datetime.strptime(test_time, time_format).strftime('%H')
        mmin = datetime.strptime(test_time, time_format).strftime('%M')
        msec = datetime.strptime(test_time, time_format).strftime('%S')
        mhour = int(hour) - int(value2[:-1])
        if mhour < 10:
            tempstr = '0' + str(mhour) + str(mmin)
        else:
            tempstr = str(mhour) + str(mmin)
        log_type('start', value = tempstr)
        log_type('end')

def _write_note(note_string, value):
    if value is not None:
        chour, cminute = _split_time_value(value)
        note_string += metadata.time(chour=chour, cminute=cminute)
    else:
        note_string += metadata.time()
    timestore.writetofile([note_string])

def _split_time_value(value):
    time = value.split(':')
    if len(time) is 2:
        return time[0], time[1]
    else:
        return value[:2], value[-2:]

def _error(state):
    try:
        s = re.search(r'(\d{4}(-\d{2}){2})T(([01]\d|2[0-3])(:[0-5]\d){2})\+(\d{4})', \
                    ''.join(timestore.readfromfile()[-1:]))
        print('You already', state + 'ed your timer!', s.group(0))
        return False
    except:
        print('You already', state + 'ed your timer!', ''.join(timestore.readfromfile()[-1:]))
        return False
