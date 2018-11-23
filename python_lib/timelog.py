from python_lib import shared, metadata, git_timestore_calls as gtc
from datetime import datetime
import re, logging


time_format = shared.get_time_format()[:-2]

def log_type(state, **kwargs):
    logging.debug(f'timelog.log_type({state}, {kwargs})')
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
    value = kwargs.get('value', None)
    cday = kwargs.get('date', None)
    username = shared.get_git_variables()['username']
    note_dict = {}
    note_dict['user'] = username  
    print(state)
    if metadata.check_correct_order(username, state) is True:
        try:
            if cday is None:
                return _state_types(state, value, note_dict)
            return _state_types(state, value, note_dict, cday = cday)
        except:
            _write_note(note_dict, value, state)
    else:
        return _error(state)
    return True

def _state_types(state, value, note_dict, **kwargs):
    logging.debug(f'timelog._state_types({state}, {value}, {note_dict}, {kwargs})')
    cday = kwargs.get('cday', None)
    if state == 'did':
        return _did_test(value)
    elif state == 'end' or state == 'start':
        if _custom_check(value) is False:
            return False
        _write_note(note_dict, value, state, cday = cday)
        return True

def _custom_check(value):
    logging.debug(f'timelog._custom_check({value})')
    if re.search(r'([01]\d|2[0-3])(:*)[0-5]\d', value):
        return True
    else:
        if re.search(r'([01]\d|2[0-3])(:*)\d', value):
            logging.error('Seems like you forgot a digit!\nPlease use the following format: hh:mm or hhmm')
            return False
        
def _did_test(value):
    logging.debug(f'timelog._did_test({value})')
    if re.search(r'((\d){1,2})([h]|[H])', value):
        value2 = re.search(r'((\d){1,2})([h]|[H])', value).group(0)
        test_time = metadata.time()[:-5]
        hour = datetime.strptime(test_time, time_format).strftime('%H')
        mmin = datetime.strptime(test_time, time_format).strftime('%M')
        date = datetime.strptime(test_time, time_format).strftime('%d')
        mhour = int(hour) - int(value2[:-1])
        if mhour < 0:
            mhour = 24 + mhour
            new_date = '0' + str((int(date) - 1))
        if mhour < 10:
            tempstr = '0' + str(mhour) + str(mmin)
        else:
            tempstr = str(mhour) + str(mmin)
        if 'new_date' in locals():
            log_type('start', value = tempstr, date = new_date)
        else:
            log_type('start', value = tempstr)
        log_type('end')
        return True
    return False

def _write_note(note_dict, value, state, **kwargs):
    logging.debug(f'timelog._write_note({note_dict}, {value}, {kwargs})')
    cday = kwargs.get('cday', None)
    if value is not None:
        chour, cminute = _split_time_value(value)
        if cday is not None:
            if state == 'start':
                note_dict['timestamp_start'] = metadata.time(chour=chour, cminute=cminute, cday=cday)
            else:
                note_dict['timestamp_start'] = metadata.time(chour=chour, cminute=cminute, cday=cday)
        else:
            if state == 'end':
                note_dict['timestamp_end'] = metadata.time(chour=chour, cminute=cminute)
            else:
                note_dict['timestamp_end'] = metadata.time(chour=chour, cminute=cminute)
    else:
        if state == 'start':
                note_dict['timestamp_start'] = metadata.time()
        elif state == 'end':
                note_dict['timestamp_end'] = metadata.time()
    print(note_dict)
    if state == 'start':
        # gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], content=note_dict) # Tilfoej ny!
        gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], remove='74866fd4078fdad62b13a4968087852aec7b0788')
    elif state == 'end':
        gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], append='sha1', content={'timestamp_end': '123'}) # tilfoej slut tid
    # shared.sha1_gen_dict(note_dict) # Generate SHA1 to store in non push namespace
    # content = gtc.get_all_by_path(shared.get_git_variables()['username'],datetime.now().year,datetime.now().month)
    
    # gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], remove='28fc3ad6e0ebe8a5a5fdd47ef9607fa7449c8f19') # remove time

def get_last_var(rtnval):
    val = gtc.get_all_as_dict()
    for each in val:
        res = 0
        id = ''
        for each2 in val[each]:
            if val[each][each2]['user'] == shared.get_git_variables()['username']:
                res += 1
                id = each2
        if (res % 2) != 0:
            return val[each][id][rtnval]



def _split_time_value(value):
    logging.debug(f'timelog._split_time_value({value})')
    try:
        time = value.split(':')
        if len(time) is 2:
            return time[0], time[1]
        else:
            return value[:2], value[-2:]
    except:
        return value[:2], value[-2:]

def _error(state):
    logging.debug(f'timelog._error({state})')
    try:
        s = re.search(r'(\d{4}(-\d{2}){2})T(([01]\d|2[0-3])(:[0-5]\d){2})[+-](\d{4})', \
                    get_last_var('timestamp'))
        logging.error('You already ' + state + 'ed your timer! ' + s.group(0))
    except:
        logging.error('You already ' + state + 'ed your timer! ')
    # logging.error('dooo')
    return False