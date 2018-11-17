import logging, subprocess, json
from . import shared, git_timestore as gt, git_timestore_merge as gtm

def store(**kwargs):
    #TODO maybe modify before passing
    content = kwargs.get('content', None)
    if type(content) is str: # In case content is json
        kwargs['content'] = json.loads(content)
    gt.store(kwargs)
    if shared.autopush():
        push()
        
def fetch():
    logging.debug(f'git_timestore_calls.fetch()')
    gtm.fetch()

def push():
    logging.debug(f'git_timestore_calls.push()')
    gtm.push()

def get_all_by_path(path):
    logging.debug(f'git_timestore_calls.get_all_by_path({path})')
    return gt.extract_entries_by_path(path)