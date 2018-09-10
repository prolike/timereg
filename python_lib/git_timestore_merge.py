import logging, subprocess, os
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
    merge_timeentries()

def _fetch_call():
    logging.debug(f'git_timestore_merge._fetch_call()')
    call = shared.git_prefix() + ['fetch', 'origin', 'refs/time/commits:refs/time/commits'] + shared.git_suffix()
    p = subprocess.run(call, stdout=subprocess.PIPE)
    return (p.returncode == 0)

def _push_call():
    logging.debug(f'git_timestore_merge._push_call()')
    call = shared.git_prefix() + ['push', 'origin', 'refs/time/commits'] + shared.git_suffix()
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

def merge_timeentries():
    '''
    Fetch remote refs/notes/commits and tries to fix any merge conflict, 
    if unsuccessful exits the program with return code 1
    '''
    logging.debug(f'git_timestore_merge.merge_timeentries()')
    _rename_ref_time_file('commits', 'temp')
    if _fetch_call():
        _merge_time_conflicts('temp')
    else:
        logging.error('Unable to fix merge conflicts, restoring files')
        rename_refs_notes_file('temp', 'commits')
        sys.exit(1)


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

    local = gt.load_git_commit_by_hash_name(local)
    remote = gt.load_git_commit_by_hash_name(remote)

    local = gt.load_git_tree_by_hash_name(local.get_tree())
    remote = gt.load_git_tree_by_hash_name(remote.get_tree())

    local_dict = local.entries_to_dict()
    remote_dict = remote.entries_to_dict()

    # in case the clone have no notes before
    if split_point is None:
        split_point_dict = {}
        distinct, overlapping = dict_find_distinct_and_overlapping(local_dict, remote_dict)        
    else:
        split_point = gt.load_git_commit_by_hash_name(split_point)
        split_point = gt.load_git_tree_by_hash_name(split_point.get_tree())
        split_point_dict = split_point.entries_to_dict()

        remote_split_point_diff = tree_hash_refrence_difference(remote_dict, split_point_dict)
        local_split_point_diff = tree_hash_refrence_difference(local_dict, split_point_dict)
        distinct, overlapping = dict_find_distinct_and_overlapping(local_split_point_diff, remote_split_point_diff)

    for key in distinct:
        if key in local_dict:
            if key not in remote_dict:
                new_entry = go.Entry('blob', local_dict[key], gt.tree_codes['file'], key)
                remote.add_entry(new_entry)
            else:
                new_entry = remote.get_entry_by_key(key)
                new_entry.p1 = local_dict[key]
                remote.change_entry_by_key(key, new_entry)

    for key in overlapping:
        if key in split_point_dict:

            out = split_point_dict[key]
            new_blob = gt.treeway_merge_blobs(split_point_dict[key], remote_dict[key], local_dict[key])
        else:
            new_blob = gt.treeway_merge_blobs(None, remote_dict[key], local_dict[key])
        
        new_entry = remote.get_entry_by_key(key)
        new_entry.p1 = new_blob
        remote.change_entry_by_key(key, new_entry)
    
    tree = remote.save_tree()
    commit = gt.commit_tree(tree)
    gt.save_commit_ref(commit)

    _delete_ref_time_file('temp')

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


def tree_hash_refrence_difference(new, original):
    '''
    Takes two git trees and returns the differences
    
    Args:
        param1(dict): new - A dictonary made by the extract_git_tree
        param1(dict): original - A dictonary made by the extract_git_tree
    
    Return:
        dict: Returns a dictonary with the keys and values from new where it differs from the original
    '''
    logging.debug(f'git_timestore_merge.tree_hash_refrence_difference({new}, {original})')
    diff = {}
    
    for key, value in new.items():
        if key not in original or original[key] != value:
            diff[key] = value
    return diff

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