from python_lib import shared
import sys
import os
import subprocess
import logging

def push_notes():
    '''
    Push git notes to remote via 'git push origin refs/notes/commits',
    and deals with any merge issues that may occur.
    '''
    fetch = fetch_notes_call()
    if fetch.returncode == 0:
        push = push_notes_call()
    elif fetch.returncode == 1:
        logging.debug('fetch failed')
        notes_merge()
        push = push_notes_call()
    
    if push.returncode != 0:
        logging.error('something went wrong in the push')
        sys.exit(1)

def fetch_notes():
    '''
    Fetches git notes from remote via 'git fetch origin refs/notes/commits:refs/notes/commits',
    and deals with any merge issues that may occur.
    '''
    fetch = fetch_notes_call()
    if fetch.returncode == 1:
        logging.debug('fetch failed')
        notes_merge()

def fetch_notes_call():
    '''
    Calls 'git fetch origin refs/notes/commits:refs/notes/commits'

    Returns:
        subprocess: with a stdout to access the output
    '''
    logging.debug('Call: git fetch origin refs/notes/commits:refs/notes/commits')
    return subprocess.run(shared.git_prefix() + ['fetch', 'origin', 'refs/notes/commits:refs/notes/commits'] + shared.git_suffix(), stdout=subprocess.PIPE)  

def push_notes_call():
    '''
    Calls 'git push origin refs/notes/commits'

    Return:
        subprocess: with a stdout to access the output
    '''
    logging.debug('Call: git push origin refs/notes/commits')
    return subprocess.run(shared.git_prefix() + ['push', 'origin', 'refs/notes/commits'] + shared.git_suffix(), stdout=subprocess.PIPE)
    
def rename_refs_notes_file(old_name, new_name):
    '''
    Rename a file in the .git/refs/notes/ folder

    Args:
        param1 (str): old_name
        param1 (str): new_name
    '''
    git_refs_notes_path = shared.get_gitpath() + 'refs/notes/'
    logging.debug(f'Call: mv .git/refs/notes/{old_name} .git/refs/notes/{new_name}')
    os.rename(git_refs_notes_path + old_name, git_refs_notes_path + new_name)

def remove_file_refs_notes(name):
    '''
    Removes a file in the .git/refs/notes/ folder with the supplied name

    Args:
        param1(str): name
    '''
    git_refs_notes_path = shared.get_gitpath() + 'refs/notes/'
    os.remove(git_refs_notes_path + name)

def notes_merge():
    '''
    Fetch remote refs/notes/commits and tries to fix any merge conflict, 
    if unsuccessful exits the program with return code 1
    '''
    rename_refs_notes_file('commits', 'temp')
    fetch = fetch_notes_call()
    if fetch.returncode == 0:
        __merge_notes_conflicts('temp')
    else:
        logging.error('Unable to fix merge conflicts, restoring files')
        rename_refs_notes_file('temp', 'commits')
        sys.exit(1)

def __merge_notes_conflicts(local_name):
    '''
    Should not be called outside this file. 
    Updates blob refrences in case of changes is not overlapping and in case of overlap it 
    merges the local note blobs into the remote by looking at the commit split_point.

    Args:
        param1(str): local_name - The name of the renamed commits file
    '''
    with open(shared.get_gitpath() +'refs/notes/' + local_name) as f:
        for line in f:
            local = line.rstrip()
    
    with open(shared.get_gitpath() +'refs/notes/commits') as f:
        for line in f:
            remote = line.rstrip()
    
    split_point = find_commit_split(local, remote)
    
    local = extract_git_tree_object(extract_git_commit_object(local)['tree'])
    remote = extract_git_tree_object(extract_git_commit_object(remote)['tree'])
    
    #in case the clone have no notes before
    if split_point is None:
        split_point = {}
        distinct, overlapping = dict_find_distinct_and_overlapping(local, remote)        
    else:
        split_point = extract_git_tree_object(extract_git_commit_object(split_point)['tree'])
        remote_split_point_diff = tree_hash_refrence_difference(remote, split_point)
        local_split_point_diff = tree_hash_refrence_difference(local, split_point)
        distinct, overlapping = dict_find_distinct_and_overlapping(local_split_point_diff, remote_split_point_diff)

    for key in distinct:
        if key in local:
            update_hashpointer_commit_call(key, local[key])
        elif key in remote:
            update_hashpointer_commit_call(key, remote[key])

    for key in overlapping:
        if key in split_point:
            merge_conflict_overlap(key, split_point[key], remote[key], local[key])
        else:
            merge_conflict_overlap(key, None, remote[key], local[key])

    remove_file_refs_notes(local_name)



def merge_conflict_overlap(commit_hashname, split_point_blob_hashname, remote_blob_hashname, local_blob_hashname):
    '''
    Merges the notes via the commit split point, remote and local blobs and force adds it to the commit

    Args:
        param1(str): commit_hashname - The name of the commit (git object)
        param2(str): split_point_blob_hashname - The name of the blob at the split point (git object)
        param3(str): remote_blob_hashname - The name of the blob at remote (git object)
        param4(str): local_blob_hashname - The name of the blob at local (git object)
    '''
    if split_point_blob_hashname != None:
        split_point_blob = extract_git_blob_object(split_point_blob_hashname)
    else:
        split_point_blob = []
    remote_blob = extract_git_blob_object(remote_blob_hashname)
    local_blob = extract_git_blob_object(local_blob_hashname)

    merged_blob_content = merge_blob_content(split_point_blob, remote_blob, local_blob)

    notes_add_force_call(commit_hashname, merged_blob_content)
    

def merge_blob_content(split_point, remote, local):
    '''
    Merges 2 list of strings together by looking at the split point they both originated from
hashname
    Args:
        param1(list containing strings): split_point - The list of strings the two other list originated from
        param2(list containing strings): remote - A list of strings
        param3(list containing strings): local - A list of strings
    
    Return:
        list: Returns a list containing strings 
    '''
    split_remote_diff = list_diff(split_point, remote)
    split_local_diff = list_diff(split_point, local)

    return split_point + split_remote_diff + split_local_diff


def list_diff(list1, list2):
    '''
    Args:
        param1(list): list1 - origin
        param2(list): list2 - list that is an extension of origin

    Return:
        list: Returns a list of objects list2 has added ontop of list1
    '''
    diff = list2[len(list1):]
    return diff

def notes_add_force_call(commit_hashname, msglist):
    '''
    Force call 'git notes add -f' with a list of strings as messages on the supplied commit

    Args:
        param1(str): commit_hashname - The name of the commit
        param2(list): msglist - The list of strings (notes) which is to be added to the commit
    '''
    call = shared.git_prefix() + ['notes', 'add', '-f'] 
    for msg in msglist:
        call.append('-m')
        call.append(f'{msg}')
    call.append(commit_hashname)
    # call += shared.git_suffix()
    update = subprocess.run(call, stdout=subprocess.PIPE)
    if update.returncode != 0:
        logging.error('Was unable to add on commit')

def update_hashpointer_commit_call(commit, blob):
    '''
    Calls 'git notes add -f -C' with the hashname of the blob which is to be added to a commit
    This function will stop the program with a returncode 1 if the git call returns a returncode 1

    Args:
        param1(str): commit - The hashname of the commit (git object)
        param1(str): blob - the hashname of the blob (git object)
    '''
    update = subprocess.run(shared.git_prefix() + ['notes', 'add', '-f', '-C', blob, commit], stdout=subprocess.PIPE)
    if update.returncode != 0:
        logging.error('Was unable to change blob on commit')
        sys.exit(1)

def dict_find_distinct_and_overlapping(dict1, dict2):
    '''
    Finds distinct and overlapping keys

    Args:
        param1 (dict): dict1
        param2 (dict): dict2
    
    Return:
        tuple: Returns a tuple containing two list of keys. Distinct and overlaiing keys.
    '''

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
    diff = {}
    for key, value in new.items():
        if original[key] != value:
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
    list_local = extract_git_notes_commits(local)
    list_remote = extract_git_notes_commits(remote)

    for item in list_remote:
        if item in list_local:
            return item

def extract_git_commit_object(object_name):
    '''
    Extracts a git commit using 'git cat-file -p <object name>'

    Args:
        param1(str): object_name

    Return:
        dict: Returns a dictionary of the commits content with the keys being ['tree', 'parant', 'author','committer'] and their values
    '''
    commit = {} 
    lines = extract_git_object(object_name).split('\n')
    for line in lines:
        commit[line.split(' ')[0]] = line.split(' ', 1)[-1]
    return commit

def extract_git_blob_object(object_name):
    '''
    Extracts a git blob using 'git cat-file -p <object name>'

    Args:
        param1(str): object_name

    Return:
        list: Returns a list of stings, theres strings are the lines in the blob object that is not empty 
    '''
    blob = []
    lines = extract_git_object(object_name).split('\n')
    for line in lines:
        if line != '':
            blob.append(line)
    return blob

def extract_git_tree_object(object_name):
    '''
    Extracts a git tree using 'git cat-file -p <object name>'

    Args:
        param1(str): object_name

    Return:
        dict: Returns a dictionary of the trees content with the keys being the commits hashname and the value being the blob hashname 
    '''
    tree = {}
    lines = extract_git_object(object_name).split('\n')
    for line in lines:
        if line != '':
            line = line.split('blob ')[1].split('\t')
            tree[line[1]] = line[0]
    return tree

def extract_git_object(object_name):
    '''
    Calls 'git cat-file -p <object name>' to extract the conent of a git object

    Args:
        param1(str): object_name

    Return:
        str: Returns a string with the objects content
    '''
    return subprocess.run(shared.git_prefix() + ['cat-file', '-p', object_name], stdout=subprocess.PIPE).stdout.decode('utf-8')

def extract_git_notes_commits(commit_hashname):
    '''
    Finds a list of the commit hashnames that the supplied commit extends.
    Using a subprocess to call 'git log <commit name>'  

    Args:
        param1(str): commit_hashname

    Return:
        list: Returns a list of strings with the hashnames of the commits
    '''
    output = subprocess.run(shared.git_prefix() + ['log', commit_hashname], stdout=subprocess.PIPE).stdout.decode('utf-8').split('commit ')[1:]
    return list(map(lambda x: x.split('\n')[0], output))    


def get_all_notes():
    '''
    Extract all git notes

    Return:
        dict: Returns a dictonary with the key being a reference to a commit and the value being a list of nodes on the commit
    '''
    with open(shared.get_gitpath() +'refs/notes/commits') as f:
        for line in f:
            commit = line.rstrip()

    commit = extract_git_commit_object(commit)
    tree = extract_git_tree_object(commit['tree'])
    notes = {}

    for key, value in tree.items():
        notes[key] = extract_git_blob_object(value)
    return notes