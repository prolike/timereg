from python_lib import shared, metadata, git_timestore_calls as gtc, git_timestore as gt
from datetime import datetime
import re, logging, json


time_format = shared.get_time_format()[:-2]

def get_input(text):
    return input(text)

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
    note_dict['issue'] = shared.get_issue_number()
    # print(state)
    # if metadata.check_correct_order(username, state) is True:
    #     try:
    #         if cday is None:
    #             return _state_types(state, value, note_dict)
    #         return _state_types(state, value, note_dict, cday = cday)
    #     except:
    #         _write_note(note_dict, value, state)
    # else:
    #     return _error(state)
    # return True
    trace = get_trace()
    if trace is not None:
        res = gtc.get_all_by_path([x.strip() for x in trace['path'].split(',')])
        if trace['sha1'] not in res:
            remove_trace()
            trace = None

    # q = input('Would you like to end it before you start a new time? y/n: ').lower().strip()   
    if state is 'start':
        if not trace:
            if _custom_check(value) is False:
                return False
            temp_note = _write_note(note_dict, value, state, cday = cday)
            trace = {}
            trace['sha1'] = shared.sha1_gen_dict(temp_note)
            username = shared.get_git_variables()['username']
            year = datetime.now().year
            month = datetime.now().month
            trace['path'] = username + ', ' + str(year) + ', ' + str(month)
            save_trace(trace)
        else: # trace found 
            logging.error('last one not ended')
            #TODO give context of the one open
            while(True):
                q = input('Would you like to end it before you start a new time? y/n: ').lower().strip()    
                if q == 'y' or q == 'yes':
                    #TODO end unfinished, remove trace, store start and save trace 
                    time_end = None
                    try:
                        chour, cminute = _split_time_value(value)
                        if cday is not None:
                            time_end = metadata.time(chour=chour, cminute=cminute, cday=cday)
                        else:
                            time_end = metadata.time(chour=chour, cminute=cminute)
                    except:
                        time_end = metadata.time()
                    gtc.store(target=[x.strip() for x in trace['path'].split(',')], append=trace['sha1'], content={'timestamp_end': time_end})
                    remove_trace()
                    temp_note = _write_note(note_dict, value, state, cday = cday)
                    trace = {}
                    trace['sha1'] = shared.sha1_gen_dict(temp_note)
                    username = shared.get_git_variables()['username']
                    year = datetime.now().year
                    month = datetime.now().month
                    trace['path'] = username + ', ' + str(year) + ', ' + str(month)
                    save_trace(trace)
                    break
                elif q == 'n' or q == 'no':
                    #TODO store start and overwrite trace
                    remove_trace()
                    temp_note = _write_note(note_dict, value, state, cday = cday)
                    trace = {}
                    trace['sha1'] = shared.sha1_gen_dict(temp_note)
                    username = shared.get_git_variables()['username']
                    year = datetime.now().year
                    month = datetime.now().month
                    trace['path'] = username + ', ' + str(year) + ', ' + str(month)
                    save_trace(trace)
                    break
    else:
        trace = get_trace()
        time_end = None
        try:
            chour, cminute = _split_time_value(value)
            if cday is not None:
                time_end = metadata.time(chour=chour, cminute=cminute, cday=cday)
            else:
                time_end = metadata.time(chour=chour, cminute=cminute)
        except:
            time_end = metadata.time()
        gtc.store(target=[x.strip() for x in trace['path'].split(',')], append=trace['sha1'], content={'timestamp_end': time_end})
        remove_trace()
    # if q == 'y':
    #     return True
    # else:
    #     return False
    # return True


def save_trace(content):
    content = json.dumps(content)
    blob = gt.Blob(content)
    ref = blob.save()
    gt.save_ref(ref, 'refs/time/trace')

def get_trace():
    ref = gt.get_current_ref('refs/time/trace')
    blob = gt.load_git_blob_by_hash(ref)
    content = blob.content
    if content == '':
        content = None
    else:
        content = json.loads(content)
    return content

def remove_trace():
    gt.remove_ref('refs/time/trace')

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
    try:
        if re.search(r'([01]\d|2[0-3])(:*)[0-5]\d', value):
            print('true')
            return True
        else:
            if re.search(r'([01]\d|2[0-3])(:*)\d', value):
                logging.error('Seems like you forgot a digit!\nPlease use the following format: hh:mm or hhmm')
                return False
    except:
        return True

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
                note_dict['timestamp_end'] = metadata.time(chour=chour, cminute=cminute, cday=cday)
        else:
            if state == 'start':
                note_dict['timestamp_start'] = metadata.time(chour=chour, cminute=cminute)
            else:
                note_dict['timestamp_end'] = metadata.time(chour=chour, cminute=cminute)
    else:
        if state == 'start':
                note_dict['timestamp_start'] = metadata.time()
        elif state == 'end':
                note_dict['timestamp_end'] = metadata.time()
    if state == 'start':
        gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], content=note_dict) # Tilfoej ny!
        # gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], remove='74866fd4078fdad62b13a4968087852aec7b0788')
    elif state == 'end':
        gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], append='sha1', content={'timestamp_end': '123'}) # tilfoej slut tid
    return note_dict
    # shared.sha1_gen_dict(note_dict) # Generate SHA1 to store in non push namespace
    # content = gtc.get_all_by_path(shared.get_git_variables()['username'],datetime.now().year,datetime.now().month)
    
    # gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], remove='28fc3ad6e0ebe8a5a5fdd47ef9607fa7449c8f19') # remove time

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