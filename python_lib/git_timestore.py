import os, sys, subprocess, logging, signal
from python_lib import shared 
from .git_objects import Entry, Blob, Commit, Tree

tree_codes = {
    'commit':   100644,
    'file':     100644
}

def save_git_object(obj):
    logging.debug(f'git_timestore.save_git_object({obj})')
    p1 = subprocess.run(shared.git_prefix() + ['hash-object', '-t', obj.get_type(),'-w', '--stdin'], \
                           stdout=subprocess.PIPE, input=str(obj), encoding='utf-8')
    hash_name = p1.stdout.rstrip()
    return hash_name
    
def save_git_blob(content):
    logging.debug(f'git_timestore.save_git_blob({content})')
    return save_git_object(content)

def save_git_tree(obj):
    logging.debug(f'git_timestore.save_git_tree({obj})')
    p1 = subprocess.run(shared.git_prefix() + ['mktree'], \
                        stdout=subprocess.PIPE, input=str(obj), encoding='utf-8')
    hash_name = p1.stdout.rstrip()
    return hash_name

def save_git_commit(commit):
    logging.debug(f'git_timestore.save_git_commit({commit})')    
    if commit.parent:
        call = shared.git_prefix() + ['commit-tree', commit.tree, '-p', commit.parent, '-m', commit.msg]
    else:
        call = shared.git_prefix() + ['commit-tree', commit.tree, '-m', commit.msg]
    
    p = subprocess.run(call, stdout=subprocess.PIPE)
    return p.stdout.decode('utf-8').rstrip()

def save_commit_ref(commit_hash):
    logging.debug(f'git_timestore.save_commit_ref({commit_hash})')
    p = subprocess.run(shared.git_prefix() + ['update-ref', 'refs/time/commits', commit_hash], \
                            stdout=subprocess.PIPE , encoding='utf-8')

def read_git_object_content(name):
    logging.debug(f'git_timestore.read_git_object_content({name})')
    p = subprocess.run(shared.git_prefix() + ['cat-file', '-p', name], shell=False, \
                        stdout=subprocess.PIPE, encoding='utf-8')
    return p.stdout.rstrip().split('\n')

def read_git_object_type(name):
    logging.debug(f'git_timestore.read_git_object_type({name})')
    return subprocess.run(shared.git_prefix() + ['cat-file', '-t', name], stdout=subprocess.PIPE,\
                          encoding='utf-8').stdout.rstrip()

def load_git_tree_by_hash_name(name):
    logging.debug(f'git_timestore.load_git_tree_by_hash_name({name})')
    tree = Tree()
    lines = read_git_object_content(name)
    entries = []
    for line in lines:
        if line == '':
            continue
        elements = line.split(' ', 3)
        p2_type = elements[0]
        p1_type = elements[1]
        elements = elements[2].split('\t')
        p1 = elements[0]
        p2 = elements[1]
        tree.add_entry(Entry(p1_type, p1, p2_type, p2))
    return tree

def load_git_blob_by_hash_name(name):
    logging.debug(f'git_timestore.load_git_blob_by_hash_name({name})')
    return read_git_object_content(name)

def load_git_commit_by_hash_name(name):
    logging.debug(f'git_timestore.load_git_commit_by_hash_name({name})')
    if name == '':
        return None
    lines = read_git_object_content(name)
    tree = lines[0].split(' ')[1]
    parent = lines[1].split(' ')[1]
    return Commit(tree, parent, '')

def get_current_ref():
    logging.debug(f'git_timestore.get_current_ref()')
    call = shared.git_prefix() + ['show-ref', 'refs/time/commits']
    p = subprocess.run(call, shell=False, stdout=subprocess.PIPE, encoding='utf-8')
    return p.stdout.rstrip().split(' ')[0]
        
def load_latest_tree():
    logging.debug(f'git_timestore.load_latest_tree()')
    commit = load_git_commit_by_hash_name(get_current_ref())
    if commit:
        return load_git_tree_by_hash_name(commit.tree)
    return Tree()

def commit_tree(tree_hashname):
    logging.debug(f'git_timestore.commit_tree({tree_hashname})')
    parent = get_current_ref()
    if parent == '':
        parent = None
    commit = Commit(tree_hashname, parent, 'added timestamps')
    return save_git_commit(commit)

def save_timeentry(messages, kwargs):
    '''
    Args: 
        param1(list): messages list og strings
        param2(str): String containing hash to a or commit or starts with issue
    '''
    logging.debug(f'git_timestore.save_timeentry({messages}, {kwargs})')
    tree = load_latest_tree()

    issue = kwargs.get('issue', None)
    issue_comment = kwargs.get('issue_comment', None)
    commit = kwargs.get('commit', None)
    #TODO add calendar/slack and files

    #create obj depending on args
    if commit:
        #TODO verify git object exsist
        obj = commit
    elif issue:
        url = shared.find_git_variables()['url'] + '/issue/' + str(issue)
        obj = save_git_blob(Blob(url))
    elif issue_comment:
        url = shared.find_git_variables()['url'] + '/issue/' + issue_comment
        obj = save_git_blob(Blob(url))

    if 'obj' not in locals():
        logging.error('Missing placement argument')
        sys.exit(1)

    #append new timestamps to blob with reference to the object
    for index, entry in enumerate(tree.get_all_entries()):
        if entry.p2 == obj:
            place = index
    
    if 'place' in locals():
        entry = tree.get_entry_by_index(place)
        msg_list = load_git_blob_by_hash_name(entry.p1)
        msg_list = list(filter(None, msg_list))
    else:
        msg_list = []
        entry = Entry('blob', None, tree_codes['commit'], obj)
    
    #Update old entry with new
    blob = save_git_blob(Blob('\n'.join(msg_list + messages))) 
    entry.p1 = blob

    if 'place' in locals():
        tree.change_entry_by_index(place, entry)
    else:
        tree.add_entry(entry)
    
    tree_hashname = tree.save_tree()
    commit_hash = commit_tree(tree_hashname)
    save_commit_ref(commit_hash)

def extract_entries():
    logging.debug(f'git_timestore.extract_entries()')
    result = {}
    tree = load_latest_tree()
    for entry in tree.get_all_entries():
        result[entry.p2] = load_git_blob_by_hash_name(entry.p1)
    return result

def treeway_merge_blobs(base, remote, local):
    logging.debug(f'git_timestore.extract_entries()')
    if base is not None:
        base = load_git_blob_by_hash_name(base)
    else:
        base = []
    remote = load_git_blob_by_hash_name(remote)
    local = load_git_blob_by_hash_name(local)

    content = merge_list_content(base, remote, local)
    blob = Blob('\n'.join(content))
    return save_git_blob(blob)


def merge_list_content(base, remote, local):
    '''
    Merges 2 list of strings together by looking at the split point they both originated from hashname
    Args:
        param1(list containing strings): base - The list of strings the two other list originated from
        param2(list containing strings): remote - A list of strings
        param3(list containing strings): local - A list of strings
    
    Return:
        list: Returns a list containing strings 
    '''
    logging.debug(f'git_timestore.merge_list_content({base}, {remote}, {local})')

    base_remote_diff = list_diff(base, remote)
    base_local_diff = list_diff(base, local)

    return base + base_remote_diff + base_local_diff


def list_diff(list1, list2):
    '''
    Args:
        param1(list): list1 - origin
        param2(list): list2 - list that is an extension of origin

    Return:
        list: Returns a list of objects list2 has added ontop of list1
    '''
    logging.debug(f'git_timestore.list_diff({list1}, {list2})')
    diff = list2[len(list1):]
    return diff