import sys
import os
import subprocess
import logging

def push_notes():
    push = push_notes_call()
    if push.returncode == 1:
        logging.debug("push failed")
        logging.debug("merge conflict")
        fetch = fetch_notes_call()
        if fetch.returncode == 1:
            logging.debug("fetch failed")
            notes_merge()
            push = push_notes_call()
            if push.returncode != 0:
                logging.error("something went wrong in the push")
                sys.exit(1)

def fetch_notes():
    fetch = fetch_notes_call()
    if fetch.returncode == 1:
        logging.debug("fetch failed")
        notes_merge()

def fetch_notes_call():
    logging.debug("Call: git fetch origin refs/notes/commits:refs/notes/commits")
    return subprocess.run(["git", "fetch", "origin", "refs/notes/commits:refs/notes/commits"], stdout=subprocess.PIPE)  

def push_notes_call():
    logging.debug("Call: git push origin refs/notes/commits")
    return subprocess.run(["git", "push", "origin", "refs/notes/commits"], stdout=subprocess.PIPE)
    
def rename_refs_notes_file(old_name, new_name):
    global gitpath
    gitpath = find_git(os.getcwd())
    git_refs_notes_path = gitpath + "refs/notes/"
    logging.debug(f"Call: mv .git/refs/notes/{old_name} .git/refs/notes/{new_name}")
    subprocess.run(["mv", git_refs_notes_path + old_name, git_refs_notes_path + new_name])

def remove_refs_notes_temp():
    git_refs_notes_path = gitpath + "refs/notes/"
    subprocess.run(["rm", git_refs_notes_path + "temp"])

def notes_merge():
    rename_refs_notes_file("commits", "temp")
    fetch = fetch_notes_call()
    if fetch.returncode == 0:
        merge_notes_conflicts()
    else:
        logging.error("Unable to fix merge conflicts, restoring files")
        rename_refs_notes_file("temp", "commits")
        sys.exit(1)

def merge_notes_conflicts():
    global gitpath
    gitpath = find_git(os.getcwd())
    local = subprocess.run(["cat", gitpath + "refs/notes/temp"], stdout=subprocess.PIPE).stdout.decode("utf-8").rstrip()
    origin = subprocess.run(["cat", gitpath + "refs/notes/commits"], stdout=subprocess.PIPE).stdout.decode("utf-8").rstrip()
    split_point = find_commit_split(local, origin)
    
    local = extract_git_tree_object(extract_git_commit_object(local)['tree'])
    origin = extract_git_tree_object(extract_git_commit_object(origin)['tree'])
    split_point = extract_git_tree_object(extract_git_commit_object(split_point)['tree'])


    origin_split_point_diff = tree_hash_refrence_difference(origin, split_point)
    local_split_point_diff = tree_hash_refrence_difference(local, split_point)

    distinct, overlapping = dict_find_distinct_and_overlapping(local_split_point_diff, origin_split_point_diff)

    for key in distinct:
        if key in local:
            update_hashpointer_commit_call(key, local[key])
        elif key in origin:
            update_hashpointer_commit_call(key, origin[key])

    for key in overlapping:
        if key in split_point:
            merge_conflict_overlap(key, split_point[key], origin[key], local[key])
        else:
            merge_conflict_overlap(key, None, origin[key], local[key])

    remove_refs_notes_temp()



def merge_conflict_overlap(commit_hashname, split_point_blob_hashname, origin_blob_hashname, local_blob_hashname):
    if split_point_blob_hashname != None:
        split_point_blob = extract_git_blob_object(split_point_blob_hashname)
    else:
        split_point_blob = []
    origin_blob = extract_git_blob_object(origin_blob_hashname)
    local_blob = extract_git_blob_object(local_blob_hashname)

    merged_blob_content = merge_blob_content(split_point_blob, origin_blob, local_blob)

    notes_add_force_call(commit_hashname, merged_blob_content)
    

def merge_blob_content(split_point, origin, local):
    split_origin_diff = list_diff(split_point, origin)
    split_local_diff = list_diff(split_point, local)

    return split_point + split_origin_diff + split_local_diff


def list_diff(list1, list2):
    diff = list2[len(list1):]
    return diff

def notes_add_force_call(commit_hashname, msglist):
    call = ['git', 'notes', 'add', '-f']
    for msg in msglist:
        call.append("-m")
        call.append(f'{msg}')
    call.append(commit_hashname)
    update = subprocess.run(call, stdout=subprocess.PIPE)
    if update.returncode != 0:
        logging.error("Was unable to add on commit")

def update_hashpointer_commit_call(commit, blob):
    update = subprocess.run(["git", "notes", "add", "-f", "-C", blob, commit], stdout=subprocess.PIPE)
    if update.returncode != 0:
        logging.error("Was unable to change blob on commit")
        sys.exit(1)

def dict_find_distinct_and_overlapping(dict1, dict2):
    '''
    Finds distinct and overlapping keys

    Args:
        param1 (dict): dict1
        param2 (dict): dict2
    
    Returns:
        tuple: The return value is a tuple containing two list of keys. Distinct and overlaiing keys.
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
    diff = {}
    for key, value in new.items():
        if original[key] != value:
            diff[key] = value
    return diff

def find_commit_split(local, origin):
    list_local = extract_git_notes_commits(local)
    list_origin = extract_git_notes_commits(origin)

    for item in list_origin:
        if item in list_local:
            return item

def extract_git_commit_object(object_name):
    commit = {} 
    lines = extract_git_object(object_name).split("\n")
    for line in lines:
        commit[line.split(" ")[0]] = line.split(" ", 1)[-1]
    return commit

def extract_git_blob_object(object_name):
    blob = []
    lines = extract_git_object(object_name).split("\n")
    for line in lines:
        if line != "":
            blob.append(line)
    return blob

def extract_git_tree_object(object_name):
    #dict with commit-hash as keys and blob-hash as value
    tree = {}
    lines = extract_git_object(object_name).split("\n")
    for line in lines:
        if line != '':
            line = line.split("blob ")[1].split("\t")
            tree[line[1]] = line[0]
    return tree

def extract_git_object(object_name):
    return subprocess.run(["git", "cat-file", "-p", object_name], stdout=subprocess.PIPE).stdout.decode("utf-8")

def extract_git_notes_commits(commit_hashname):
    output = subprocess.run(["git", "log", commit_hashname], stdout=subprocess.PIPE).stdout.decode("utf-8").split("commit ")[1:]
    return list(map(lambda x: x.split("\n")[0], output))    

def find_git(path):
    if os.path.isdir(path + "/.git/"):
        return path + "/.git/"
    else:
        strlist = path.split('/')
        newpath = "/".join(strlist[:-1])
        return find_git(newpath)