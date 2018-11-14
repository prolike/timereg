import logging, subprocess, json
from . import shared, git_timestore as gt, git_timestore_merge as gtm

def store(**kwargs):
    #TODO maybe modify before passing
    content = kwargs.get('content', None)
    if type(content) is str: # In case content is json
        kwargs['content'] = json.loads(content)
    gt.store(kwargs)
    
    #TODO remove later
    # gt.store(target=['alfen','2018','november2018'], content={'user':'alfen2', 'context':'issue 1','start':'11-11-2018UTC12-00-00'})
    # gt.test(target=['alfen','1'], remove='aabef5906871f40ab246195a624dc915650ca88d')
    # gt.test(target=['alfen','1'], \
    # append='ba218542e62af25ac1ba888c5d09fc1a182e4117', \
    # content={'end':'11-11-2018UTC12-00-00'})

# def store(**kwargs):
#     logging.debug(f'git_timestore_calls.store({kwargs})')
#     print(kwargs)
    # gt.save_entry(kwargs)
    # if shared.autopush():
    #     push()

# def store_json(json_string):
#     logging.debug(f'git_timestore_calls.store_json({json_string})')
#     json_data = json.loads(json_string)
#     if 'repo' in json_data['storage']:
#         shared.set_working_dir(json_data['storage'].pop('repo'))
#     kwargs = {}
#     kwargs['entry'] = json_data['content']
#     for key, value in json_data['storage'].items():
#         kwargs[key] = value
#     gt.save_entry(kwargs)
#     if shared.autopush():
#         push()

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