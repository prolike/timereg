import logging, subprocess
from . import shared, git_timestore as gt, git_timestore_merge as gtm 

def store(messages, **kwargs):
    logging.debug(f'git_timestore_calls.store({messages}, {kwargs})')
    gt.save_timeentry(messages, kwargs)

def get_all():
    logging.debug(f'git_timestore_calls.get_all()')
    return gt.extract_entries()

def fetch():
    logging.debug(f'git_timestore_calls.fetch()')
    gtm.fetch()

def push():
    logging.debug(f'git_timestore_calls.push()')
    gtm.push()