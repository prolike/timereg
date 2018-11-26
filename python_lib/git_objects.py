from . import git_timestore as gt, shared


class Tree:

    def __init__(self):
        self.entries = []

    def __str__(self):
        result = ''
        for entry in self.entries:
            result += str(entry)
        return result

    def get_blob_obj(self, path):
        '''
        Finds and returns the desired obj based on the path(list),
        if object does not exist it will be created
        Args:
            param1(list): path - a list of strings to the desired path in the tree
        
        Return:
            Blob or Tree: Returns a blob or tree object of the desired path
        '''
        if type(path) == list:
            if len(path) is 0:
                return
            elif len(path) is 1:
                obj = self.get_blob_entry_by_name(str(path[0]))
                if obj is None:
                    #create new entry
                    obj = Entry('blob', '', '100644', path[0])
                    self.add_entry(obj)
                    obj.content = Blob('{ }')
                return obj.get_content()
            elif len(path) > 1:
                obj = self.get_tree_entry_by_name(str(path[0]))
                if obj is None:
                    #create new entry
                    obj = Entry('tree', '', '040000', path[0])
                    self.add_entry(obj)
                    obj.content = Tree()
                return obj.get_content().get_blob_obj(path[1:])
    def save(self):
        #recursively saves all edits and returns the ref for the new tree
        for entry in self.entries:
            entry.save()
        return gt.save_git_tree(self)

    def get_type(self):
        return 'tree'

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_all_entries(self):
        return self.entries

    def get_blob_entry_by_name(self, name):
        #TODO new
        for entry in self.entries:
            if entry.p2 == name and entry.p1_type == 'blob':
                return entry
    
    def get_tree_entry_by_name(self, name):
        #TODO new
        for entry in self.entries:
            if entry.p2 == name and entry.p1_type == 'tree':
                return entry
    
    def get_entry_by_key(self, key):
        for entry in self.entries:
            if entry.p2 == key:
                return entry

    def change_entry_by_key(self, key, new_entry):
        for i, entry in enumerate(self.entries):
            if entry.p2 == key:
                self.entries[i] = new_entry
                return
                
    def entries_to_dict(self):
        result = {}
        for entry in self.entries:
            result[entry.p2 + '-' + entry.p1_type] = entry.p1
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
    
    def save(self):
        #TODO new
        return gt.save_git_blob(self)

    def __str__(self):
        return self.content

class Entry:
    def __init__(self, p1_type, p1, p2_type, p2):
        self.p1_type = p1_type #tree or blob
        self.p1 = p1 #git hash
        self.p2_type = p2_type #treecode
        self.p2 = p2 #str
        self.content = None

    def load_content(self):
        #TODO new
        if self.p1_type == 'tree':
            self.content = gt.load_git_tree_by_hash(self.p1)
        if self.p1_type == 'blob':
            self.content = gt.load_git_blob_by_hash(self.p1)

    def get_content(self):
        #TODO new
        if self.content is None:
            self.load_content()
        return self.content
    
    def content_is_loaded(self):
        #TODO new
        return self.content is not None
    
    def save(self):
        #TODO new
        if self.content_is_loaded():
            self.p1_type = self.content.get_type()
            self.p1 = self.content.save()
            self.content = None

    def __str__(self):
        return f'{self.p2_type} {self.p1_type} {self.p1}\t{self.p2}\n'