import logging, subprocess, json
from . import shared, git_timestore as gt, git_timestore_merge as gtm

def store(**kwargs):
    logging.debug(f'git_timestore_calls.store({kwargs})')
    gt.save_entry(kwargs)
    if shared.autopush():
        push()

def store_json(json_string):
    logging.debug(f'git_timestore_calls.store_json({json_string})')
    json_data = json.loads(json_string)
    if 'repo' in json_data['storage']:
        shared.set_working_dir(json_data['storage'].pop('repo'))
    kwargs = {}
    kwargs['entry'] = json_data['content']
    for key, value in json_data['storage'].items():
        kwargs[key] = value
    gt.save_entry(kwargs)
    if shared.autopush():
        push()

def fetch():
    logging.debug(f'git_timestore_calls.fetch()')
    gtm.fetch()

def push():
    logging.debug(f'git_timestore_calls.push()')
    gtm.push()

def get_all_as_dict():
    logging.debug(f'git_timestore_calls.get_all_as_dict()')
    return gt.extract_entries()

def get_all_by_hash(hashname):
    logging.debug(f'git_timestore_calls.get_all_by_hash({hashname})')
    return gt.extract_entries_by_hash(hashname)