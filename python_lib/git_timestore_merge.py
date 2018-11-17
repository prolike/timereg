import logging, subprocess, os, sys, json
from . import shared, git_objects as go, git_timestore as gt


def fetch():
    logging.debug(f'git_timestore_merge.fetch()')
    if not _fetch_call():
        merge()

def push():
    logging.debug(f'git_timestore_merge.push()')
    if not _push_call():
        logging.error('Unable to push')
        if not _fetch_call():
            merge()
            if not _push_call():
                logging.warning('Rollback')
                _rename_ref_time_file('temp', 'commits')

def merge():
    logging.debug(f'git_timestore_merge.merge()')
    logging.warning('Merging time entries')
    merge_time_trees()

def _fetch_call():
    logging.debug(f'git_timestore_merge._fetch_call()')
    call = shared.git_prefix() \
           + ['fetch', 'origin', 'refs/time/commits:refs/time/commits'] \
           + shared.git_suffix()
    p = subprocess.run(call, stdout=subprocess.PIPE)
    return (p.returncode == 0)

def _push_call():
    logging.debug(f'git_timestore_merge._push_call()')
    call = shared.git_prefix() \
           + ['push', 'origin', 'refs/time/commits'] \
           + shared.git_suffix()
    p = subprocess.run(call, stdout=subprocess.PIPE)
    return (p.returncode == 0)

def _rename_ref_time_file(old_name, new_name):
    '''
    Rename a file in the .git/refs/time/ folder

    Args:
        param1 (str): old_name
        param1 (str): new_name
    '''
    logging.debug(f'git_timestore_merge._rename_ref_time_file({old_name}, {new_name})')
    git_refs_time_path = shared.get_gitpath() + 'refs/time/'
    os.rename(git_refs_time_path + old_name, git_refs_time_path + new_name)

def _delete_ref_time_file(name):
    logging.debug(f'git_timestore_merge._delete_ref_time_file({name})')
    git_refs_time_path = shared.get_gitpath() + 'refs/time/'
    os.remove(git_refs_time_path + name)

def merge_time_trees():
    '''
    Fetch remote refs/notes/commits and tries to fix any merge conflict, 
    if unsuccessful exits the program with return code 1
    '''
    logging.debug(f'git_timestore_merge.merge_time_trees()')
    _rename_ref_time_file('commits', 'temp')
    if _fetch_call():
        _merge_time_conflicts('temp')
    else:
        logging.error('Unable to fix merge conflicts, restoring files')
        _rename_ref_time_file('temp', 'commits')
        sys.exit(1)


def commit_history(commit_hashname):
    '''
    Finds a list of the commit hashnames that the supplied commit extends.
    Using a subprocess to call 'git log <commit name>'  

    Args:
        param1(str): commit_hashname

    Return:
        list: Returns a list of strings with the hashnames of the commits
    '''
    logging.debug(f'git_timestore_merge.commit_history({commit_hashname})')
    output = subprocess.run(shared.git_prefix() + ['log', commit_hashname], \
                            stdout=subprocess.PIPE, encoding='utf-8').stdout.split('commit ')[1:]
    return list(map(lambda x: x.split('\n')[0], output))  

def find_commit_split(local, remote):
    '''
    Finds the lates commen point searching from index 0

    Args:
        param1(list): local 
        param1(list): remote
    
    Return:
        str: Returns the first commen element of the two lists
    '''
    logging.debug(f'git_timestore_merge.find_commit_split({local}, {remote})')
    list_local = commit_history(local)
    list_remote = commit_history(remote)
    
    for item in list_remote:
        if item in list_local:
            return item


def merge_dict_content(base, remote, local):
    '''
    Merges 2 list of strings together by looking at the split point they both originated from hashname
    Args:
        param1(dict): base 
        param2(dict): remote 
        param3(dict): local
    
    Return:
        list: Returns a dict 
    '''
    logging.debug(f'git_timestore_merge.merge_dict_content({base}, {remote}, {local})')
    removed, added = dict_diff(base, local)
    for val in removed:
        try:
            remote.pop(val)
        except:
            pass
    for val in added:
        remote[val] = local[val]    
    return remote

def dict_diff(dict1, dict2):
    '''
    Takes 2 dicts and sort the keys dict2 has remove and added into 2 list of strings
    Args:
        param1(list): dict1 - origin
        param2(list): dict2 - list that is an extension of origin

    Return:
        list, list: Returns 2 list of keys, with the 1st being what dict2 has removed and the 2nd being what it has added
    '''
    logging.debug(f'git_timestore_merge.list_diff({dict1}, {dict2})')
    removed = []
    for key in dict1:
        if key not in dict2:
            removed.append(key)
    added = []
    for key in dict2:
        if key not in dict1:
            added.append(key)
    return removed, added

def three_way_merge_blob(origin, remote, local):
    remote_dict = json.loads(remote.content)
    local_dict = json.loads(local.content)
    if origin is not None:
        origin_dict = origin.content
    else:
        origin_dict = {}
    content = str(merge_dict_content(origin_dict, remote_dict, local_dict)).replace('\'','"')
    return gt.Blob(content)

def three_way_merge_tree(origin, remote, local):
    remote_entries_dict = remote.entries_to_dict()
    local_entries_dict = local.entries_to_dict()

    if origin is not None:
        # split point exsist
        origin_entries_dict = origin.entries_to_dict()

        remote_diff = tree_difference(origin_entries_dict, remote_entries_dict)
        local_diff = tree_difference(origin_entries_dict, local_entries_dict)
        
        distinct, overlapping = dict_find_distinct_and_overlapping(local_diff, remote_diff)
    else:
        origin_entries_dict = {}
        distinct, overlapping = dict_find_distinct_and_overlapping(local_entries_dict, \
                                                                   remote_entries_dict)

    for key in distinct:
        temp = key.rsplit('-', 1)
        
        if temp[1] == 'blob':
            entry = remote.get_blob_entry_by_name(temp[0])
        elif temp[1] == 'tree':
            entry = remote.get_tree_entry_by_name(temp[0])
        if entry is not None:
            entry.p1 = local_entries_dict[key]
        else:
            if temp[1] == 'blob':
                entry = remote.add_entry(gt.Entry('blob', local_entries_dict[key], \
                                                  '100644', temp[0]))
            elif temp[1] == 'tree':
                entry = remote.add_entry(gt.Entry('tree', local_entries_dict[key], \
                                                  '040000', temp[0]))
    
    for key in overlapping:
        temp = key.rsplit('-', 1)
        
        if temp[1] == 'blob':
            try:
                o = origin.get_blob_entry_by_name(temp[0]).get_content()
            except:
                o = None
            r = remote.get_blob_entry_by_name(temp[0]).get_content()
            l = local.get_blob_entry_by_name(temp[0]).get_content()
            remote.get_blob_entry_by_name(temp[0]).content = three_way_merge_blob(o, r, l)
        elif temp[1] == 'tree':
            try:
                o = origin.get_tree_entry_by_name(temp[0]).get_content()
            except:
                o = None
            r = remote.get_tree_entry_by_name(temp[0]).get_content()
            l = local.get_tree_entry_by_name(temp[0]).get_content()
            remote.get_tree_entry_by_name(temp[0]).p1 = three_way_merge_tree(o, r, l)

    return remote.save()

def _merge_time_conflicts(local_name):
    '''
    Should not be called outside this file. 
    Updates blob refrences in case of changes is not overlapping and in case of overlap it 
    merges the local note blobs into the remote by looking at the commit split_point.

    Args:
        param1(str): local_name - The name of the renamed commits file
    '''
    logging.debug(f'git_timestore_merge._merge_time_conflicts({local_name})')

    timepath = shared.get_gitpath() +'refs/time/' 

    with open(timepath + local_name) as f:
        for line in f:
            local = line.rstrip()
    
    with open(timepath + '/commits') as f:
        for line in f:
            remote = line.rstrip()
    
    split_point = find_commit_split(local, remote)

    local = gt.load_git_commit_by_hash(local)
    remote = gt.load_git_commit_by_hash(remote)
    
    local = gt.load_git_tree_by_hash(local.get_tree())
    remote = gt.load_git_tree_by_hash(remote.get_tree())
    try:
        split_point = gt.load_git_commit_by_hash(split_point)
        split_point = gt.load_git_tree_by_hash(split_point.get_tree())
    except:
        split_point = None

    new_ref = three_way_merge_tree(split_point, remote, local)
    gt.save_commit_ref(gt.commit_tree(new_ref))
    _delete_ref_time_file(local_name)

def tree_difference(origin, desendent):
    diff = {}
    for key, value in desendent.items():
        if key in origin:
            if origin[key] != value:
                diff[key] = value
        else:
                diff[key] = value
    return diff


def dict_find_distinct_and_overlapping(dict1, dict2):
    '''
    Finds distinct and overlapping keys

    Args:
        param1 (dict): dict1
        param2 (dict): dict2
    
    Return:
        tuple: Returns a tuple containing two list of keys. Distinct and overlaiing keys.
    '''
    logging.debug(f'git_timestore_merge.dict_find_distinct_and_overlapping({dict1}, {dict2})')

    distinct = []
    overlapping = []
    for key, value in dict1.items():
        if key in dict2:
            if dict2[key] != value:
                overlapping.append(key)
            else:
                distinct.append(key)
        else:
                distinct.append(key)
    for key, value in dict2.items():
        if key not in dict2:
            distinct.append(key)
    return (distinct, overlapping)