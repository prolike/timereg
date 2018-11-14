import os, sys, subprocess, logging, re, json
from . import shared 
from .git_objects import Entry, Blob, Commit, Tree

# tree_codes = {
#     'commit':   '100644',
#     'file':     '100644',
#     'ref':      '100644',
#     'dir':      '040000'
# }

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

# def load_git_jsonblob_by_hash(name):
#     #TODO should be removed
#     '''
#     Returns a dict in form of the json
#     '''
#     logging.debug(f'git_timestore.load_git_jsonblob_by_hash({name})')
#     return json.loads(read_git_object_content(name))

def load_git_commit_by_hash(name):
    logging.debug(f'git_timestore.load_git_commit_by_hash({name})')
    if name == '':
        return None
    lines = read_git_object_content(name).split('\n')
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
    commit = load_git_commit_by_hash(get_current_ref())
    if commit:
        return load_git_tree_by_hash(commit.tree)
    return Tree()

def commit_tree(tree_hashname):
    logging.debug(f'git_timestore.commit_tree({tree_hashname})')
    parent = get_current_ref()
    if parent == '':
        parent = None
    commit = Commit(tree_hashname, parent, 'added timestamps')
    return save_git_commit(commit)


# def edit_json_git_blob(args):
#     target = args.get('target', None)
#     remove = args.get('remove', None)
#     new_entry = args.get('entry', None)
#     tree = args['tree']

#     # TODO target for folders
#     if target:
#         new_blob_ref = ''
#     #     target_entry = tree.get_entry_by_key(target)
#     #     if target_entry:
#     #         target_blob_ref = target_entry.p1
#     #         entries = load_git_jsonblob_by_hash(target_blob_ref)

#     #         if remove:
#     #             entries.pop(remove)
#     #         if new_entry:
#     #             entries[shared.sha1_gen_dict(new_entry)] = new_entry
            
#     #         #TODO sort entries by timestamp before writing to blob
            
#     #         blob = Blob(str(entries).replace('\'','"'))
#     #         new_blob_ref = save_git_blob(blob)
#     #         target_entry.p1 = new_blob_ref

#     #         tree.change_entry_by_key(target_entry.p2 ,target_entry)
#     #         tree_ref = tree.save()
#     #         commit_ref = commit_tree(tree_ref)
#     #         save_commit_ref(commit_ref)
#     #     else:
#     #         entries = {}
#     #         if new_entry:
#     #             entries[shared.sha1_gen_dict(new_entry)] = new_entry
#     #         blob = Blob(str(entries).replace('\'','"'))
#     #         new_blob_ref = save_git_blob(blob)
#     #         target_entry = Entry('blob', new_blob_ref, tree_codes['ref'], target)
#     #         tree.add_entry(target_entry)
#     #         tree_ref = tree.save()
#     #         commit_ref = commit_tree(tree_ref)
#     #         save_commit_ref(commit_ref)
#         return new_blob_ref
#     else:
#         logging.error('Missing args')
#         sys.exit(1)
#         return

# def target_obj(args):
#     '''
#     Determins if a reference to object is send in or if it has to make a new git object.
#     And returns the reference of the target git object
#     '''
#     # logging.debug(f'git_timestore.target_obj({args})')
#     # issue = args.get('issue', None)
#     # issue_comment = args.get('issue_comment', None)
#     # commit = args.get('commit', None)
    
#     # #create obj depending on args
#     # if commit:
#     #     #TODO verify git object exsist
#     #     obj = commit
#     # elif issue:
#     #     url = shared.find_git_variables()['url'] + '/issue/' + str(issue)
#     #     obj = save_git_blob(Blob(url))
#     # elif issue_comment:
#     #     url = shared.find_git_variables()['url'] + '/issue/' + issue_comment
#     #     obj = save_git_blob(Blob(url))
#     obj_ref = ''
#     #TODO find or create ref for existing or new content storage 
#     if 'obj' not in locals():
#         logging.error('Missing placement argument')
#         sys.exit(1)
#     else:
#         return obj_ref

# def save_entry(kwargs):
#     '''
#     new time entry: 
#         entry(dict)
#         target(list)

#     remove time entry:
#         target(list)
#         remove(line hash value)
    
#     remove time entry can be done at the sametime as new time entry like an edit
#     '''
    
#     logging.debug(f'git_timestore.save_timeentry({kwargs})')
#     kwargs['tree'] = load_latest_tree()
    
    

#     # entry = kwargs.get('entry', None)
#     # json_string = kwargs.get('json', None)
#     # if json_string and not entry:
#     #     json_data = json.loads(json_string)
#     #     if 'content' in json_data:
#     #         entry = json_data['content']
#     #     else:
#     #         entry = json_data
#     #     kwargs['entry'] = entry

#     target = kwargs.get('target', None)
#     if not target:
#         target = target_obj(kwargs)
#         kwargs['target'] = target

#     new_content_ref = edit_json_git_blob(kwargs)
#     store_new_ref(new_content_ref, kwargs)

# def store_new_ref(new_content_ref, kwargs):
#     pass

# def extract_entries():
#     logging.debug(f'git_timestore.extract_entries()')
#     result = {}
#     tree = load_latest_tree()
#     for entry in tree.get_all_entries():
#         result[entry.p2] = load_git_jsonblob_by_hash(entry.p1)
#     return result

# def extract_entries_by_hash(hashname):
#     tree = load_latest_tree()
#     entry = tree.get_entry_by_key(hashname)
#     data = load_git_jsonblob_by_hash(entry.p1)
#     return data

# def treeway_merge_blobs(base, remote, local):
#     logging.debug(f'git_timestore.extract_entries()')
#     if base is not None:
#         base = load_git_jsonblob_by_hash(base)
#     else:
#         base = []
#     remote = load_git_jsonblob_by_hash(remote)
#     local = load_git_jsonblob_by_hash(local)

#     content = merge_dict_content(base, remote, local)
#     blob = Blob(str(content).replace('\'','"'))
#     return save_git_blob(blob)

# def merge_dict_content(base, remote, local):
#     '''
#     Merges 2 list of strings together by looking at the split point they both originated from hashname
#     Args:
#         param1(dict containing strings): base - The dict of strings the two other dict originated from
#         param2(dict containing strings): remote - A dict of strings
#         param3(dict containing strings): local - A dict of strings
    
#     Return:
#         list: Returns a list containing strings 
#     '''
#     logging.debug(f'git_timestore.merge_dict_content({base}, {remote}, {local})')

#     local_removed, local_added = dict_diff(base, local)
#     #TODO modify remote with the lines removed and lines added
#     for key in local_removed:
#         remote.pop(key)
#     for key in local_added:
#         remote[key] = local[key]
#     return remote 

# def dict_diff(dict1, dict2):
#     '''
#     Takes 2 dicts and sort the keys dict2 has remove and added into 2 list of strings
#     Args:
#         param1(list): dict1 - origin
#         param2(list): dict2 - list that is an extension of origin

#     Return:
#         list, list: Returns 2 list of keys, with the 1st being what dict2 has removed and the 2nd being what it has added
#     '''
#     logging.debug(f'git_timestore.list_diff({dict1}, {dict2})')
#     #TODO find added and removed keys
#     removed = []
#     for key in dict1:
#         if key not in dict2:
#             removed.append(key)
#     added = []
#     for key in dict2:
#         if key not in dict1:
#             added.append(key)
#     return removed, added

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
    print(content_blob.content)
    tree_ref = tree.save()
    save_commit_ref(commit_tree(tree_ref))