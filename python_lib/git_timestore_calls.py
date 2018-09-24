import logging, subprocess, json
from . import shared, git_timestore as gt, git_timestore_merge as gtm
from .git_objects import Time_entry

# def store(messages, **kwargs):
#     logging.debug(f'git_timestore_calls.store({messages}, {kwargs})')
#     gt.save_timeentry(messages, kwargs)

def store(**kwargs):
    logging.debug(f'git_timestore_calls.store({kwargs})')
    gt.save_entry(kwargs)

def store_json(json_string):
    logging.debug(f'git_timestore_calls.store_json({json_string})')
    json_data = json.loads(json_string)
    shared.set_working_dir(json_data['storage'].pop('repo'))
    kwargs = {}
    entry = Time_entry()
    entry.content = json_data['content']
    kwargs['entry'] = entry

    for key, value in json_data['storage'].items():
        kwargs[key] = value
    gt.save_entry(kwargs)


def fetch():
    logging.debug(f'git_timestore_calls.fetch()')
    gtm.fetch()

def push():
    logging.debug(f'git_timestore_calls.push()')
    gtm.push()

def get_all_as_dict():
    logging.debug(f'git_timestore_calls.get_all_as_dict()')
    return gt.extract_entries()

def get_all_as_list():
    logging.debug(f'git_timestore_calls.get_all_as_list()')
    return gt.entries_all_as_list()

def get_all_by_hash(hashname):
    logging.debug(f'git_timestore_calls.get_all_by_hash({hashname})')
    return gt.extract_entries_by_hash(hashname)

# def split_times_end_start(los):
#     logging.debug(f'git_timestore_calls.split_times_end_start({los})')
#     return gt.listsplitter(los)