from . import git_timestore, shared
import json


class Tree:

    def __init__(self):
        self.entries = []

    def __str__(self):
        result = ''
        for entry in self.entries:
            result += str(entry)
        return result
    
    def save_tree(self):
            return git_timestore.save_git_tree(self)

    def get_type(self):
        return 'tree'

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_all_entries(self):
        return self.entries

    def get_entry_by_index(self, index):
        return self.entries[index]
    
    def get_entry_by_key(self, key):
        for entry in self.entries:
            if entry.p2 == key:
                return entry

    def change_entry_by_index(self, index, new_entry):
        if index < len(self.entries) and index >= 0:
            self.entries[index] = new_entry

    def change_entry_by_key(self, key, new_entry):
        for i, entry in enumerate(self.entries):
            if entry.p2 == key:
                self.entries[i] = new_entry
                return
                
    def entries_to_dict(self):
        result = {}
        for entry in self.entries:
            result[entry.p2] = entry.p1
        return result


class Commit:
    def __init__(self, tree, parent, msg):
        self.tree = tree
        self.parent = parent
        self.msg = msg
    
    def get_tree(self):
        return self.tree

    def __str__(self):
        return f'tree:{self.tree} parent:{self.parent} msg:{self.msg}'

class Blob:
    def __init__(self, content):
        self.content = content

    def get_type(self):
        return 'blob'
    
    def __str__(self):
        return self.content

class Entry:
    def __init__(self, p1_type, p1, p2_type, p2):
        self.p1_type = p1_type #tree or blob
        self.p1 = p1 #git hashname
        self.p2_type = p2_type #treecode
        self.p2 = p2 #str

    def __str__(self):
        return f'{self.p2_type} {self.p1_type} {self.p1}\t{self.p2}\n'


class Time_entry:
    def __init__(self):
        self.repo = ''
        self.parent = ''
        self.content = {}

    def __str__(self):
        return str(self.content).replace('\'','"')

    def load_from_json(self, json_string):
        json_data = json.loads(json_string)
        self.content = json_data['content']

    def contenthash(self):
        return shared.sha1_gen(str(self.content))