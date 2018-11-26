import os, sys, subprocess, logging, re, json
from . import shared 
from .git_objects import Entry, Blob, Commit, Tree


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

def save_ref(commit_hash, path):
    logging.debug(f'git_timestore.save_ref({commit_hash}, {path})')
    p = subprocess.run(shared.git_prefix() + ['update-ref', path, commit_hash], \
                            stdout=subprocess.PIPE , encoding='utf-8')

def remove_ref(path):
    logging.debug(f'git_timestore.remove_ref({path})')
    p = subprocess.run(shared.git_prefix() + ['update-ref', '-d', path], \
                            stdout=subprocess.PIPE , encoding='utf-8')

def read_git_object_content(name):
    logging.debug(f'git_timestore.read_git_object_content({name})')
    p = subprocess.run(shared.git_prefix() + ['cat-file', '-p', name], shell=False, \
                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding='utf-8')
    return p.stdout.rstrip()

def read_git_object_type(name):
    logging.debug(f'git_timestore.read_git_object_type({name})')
    return subprocess.run(shared.git_prefix() + ['cat-file', '-t', name], stdout=subprocess.PIPE,\
                          encoding='utf-8').stdout.rstrip()

def load_git_tree_by_hash(name):
    logging.debug(f'git_timestore.load_git_tree_by_hash({name})')
    tree = Tree()
    lines = read_git_object_content(name).split('\n')
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

def load_git_blob_by_hash(name):
    logging.debug(f'git_timestore.load_git_blob_by_hash({name})')
    return Blob(read_git_object_content(name))

def load_git_commit_by_hash(name):
    logging.debug(f'git_timestore.load_git_commit_by_hash({name})')
    if name == '':
        return None
    lines = read_git_object_content(name).split('\n')
    tree = lines[0].split(' ')[1]
    parent = lines[1].split(' ')[1]
    return Commit(tree, parent, '')

def get_current_ref(path):
    logging.debug(f'git_timestore.get_current_ref({path})')
    call = shared.git_prefix() + ['show-ref', path]
    p = subprocess.run(call, shell=False, stdout=subprocess.PIPE, encoding='utf-8')
    return p.stdout.rstrip().split(' ')[0]
        
def load_latest_tree():
    logging.debug(f'git_timestore.load_latest_tree()')
    commit = load_git_commit_by_hash(get_current_ref('refs/time/commits'))
    if commit:
        return load_git_tree_by_hash(commit.tree)
    return Tree()

def commit_tree(tree_hashname):
    logging.debug(f'git_timestore.commit_tree({tree_hashname})')
    parent = get_current_ref('refs/time/commits')
    if parent == '':
        parent = None
    commit = Commit(tree_hashname, parent, 'added timestamps')
    return save_git_commit(commit)

def store(kwargs):
    '''

    New entry:
        path(list)
        content(dict)
    
    Append to entry:
        path(list)
        content(dict)
        append(str) - hash of the object you want to append to

    Remove entry:
        path(list)
        remove(str) - hash of the object you want to remove

        optional: - in case you want to replace an existing
            content(dict)

    '''
    logging.debug(f'git_timestore.store({kwargs})')
    tree = load_latest_tree()

    target = kwargs.get('target', None)
    if target is None:
        logging.error('Missing target arg')
        return
    content_blob = tree.get_blob_obj(target)
    if content_blob.get_type() is not 'blob':
        logging.error('Not a pblob file')
        return

    content = json.loads(content_blob.content)
    
    remove = kwargs.get('remove', None)
    if remove is not None:
        try:
            content.pop(remove)
        except:
            logging.error(f'Can\'t remove {remove} not in dict')

    append = kwargs.get('append', None)
    new_content = kwargs.get('content', None)
    if new_content is not None:
        #append
        if append is not None:
            try:
                old_content = content.pop(append)
                old_content.update(new_content)        
                key = shared.sha1_gen_dict(old_content)
                content[key] = old_content
            except:
                logging.error(f'key {append} not in dict')
        #insert new content
        else:
            key = shared.sha1_gen_dict(new_content)
            content[key] = new_content
    

    #done with content and inserts it into the blob again
    content_blob.content = json.dumps(content)
    tree_ref = tree.save()
    save_ref(commit_tree(tree_ref), 'refs/time/commits')

def extract_entries_by_path(path):
    tree = load_latest_tree()
    content_blob = tree.get_blob_obj(path)
    return json.loads(content_blob.content)