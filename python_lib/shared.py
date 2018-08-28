import os
import subprocess

gitpath = ''
working_dir = os.getcwd()
git_variables = {}
quiet_mode = False
time_format = '%Y-%m-%dT%H:%M:%S%z'

def set_working_dir(path):
    '''
    Changes the working directory to the provided path.
    Works with full path and relative from current working directory.
    Used in the -C parameter to use git commands from other folders than the current
    '''
    global working_dir, gitpath
    gitpath = ''
    working_dir = path_routing(path)

def path_routing(path):
    '''
    Takes a path and find the full path for the directory. 

    Args:
        param1(str): path

    Retrun:
        str: Returns a string with the full path
    '''
    if path[-1] == '/':
        path = path[:-1]

    if path[:1] == '/':
        return path
    elif path[:3] == '../':
        return path_up_level(os.getcwd(), path)
    elif path[:2] == './':
        return os.getcwd() + path[1:]
    
    return os.getcwd() + path

def path_up_level(cwd, path):
    if path[:3] == '../':
        return path_up_level('/'.join(cwd.split('/')[:-1]), path.split('/',1)[1])
    else:
        return cwd + '/' + path

def get_work_dir():
    return working_dir

def get_gitpath():
    global gitpath
    if gitpath == '':
        gitpath = find_git(working_dir)

    return gitpath    

def set_quiet_mode(mode):
    global quiet_mode
    quiet_mode = mode

def git_suffix():
    '''
    Send a list of suffixes in this case --quiet to mute commands if quiet mode is turned on

    Return:
        list: Returns a list of suffixes to git commands
    '''
    if quiet_mode:
        return ['--quiet']
    else:
        return []

def find_git(path):    
    '''
    Finds the full path to the .git folder in the suppiled path,
    this function starts in the supplied folder and move out untill it finds the .git folder

    Args:
        param1(str): path - The path to the folder you want to find the .git folder

    Return:
        str: Returns a string of the path to the .git folder
    '''
    if os.path.isdir(path + '/.git/'):
        return path + '/.git/'
    else:
        strlist = path.split('/')
        newpath = '/'.join(strlist[:-1])
        return find_git(newpath)

def get_git_variables():
    global git_variables
    if git_variables == {}:
        git_variables = find_git_variables()

    return git_variables

def find_git_variables():
    '''
    Makes a dictonary containing information fetched from different git configs

    Return:
        dictonary: returns branch, url, and git username, with the following keys:
        'branch', 'url', 'username'
    '''
    variables_temp = {}
    branch = subprocess.run(git_prefix() + \
                            ['rev-parse', '--abbrev-ref', 'HEAD', '--'], \
                            stdout=subprocess.PIPE)
    url = subprocess.run(git_prefix() + \
                         ['config', '--get', 'remote.origin.url'], \
                         stdout=subprocess.PIPE)
    username = subprocess.run(git_prefix() + \
                              ['config', 'github.user'], \
                              stdout=subprocess.PIPE)
    variables_temp['branch'] = branch.stdout.decode('utf-8').rstrip()[:-3]
    variables_temp['url'] = url.stdout.decode('utf-8').rstrip()
    variables_temp['username'] = username.stdout.decode('utf-8').rstrip()
    return variables_temp

def git_prefix():
    '''
    Makes the prefix -C param if needed to use all git commands in another folder than the cwd

    Retrun:
        list: Returns a list with the prefixes for git calls 
    '''
    if os.getcwd() != working_dir:
        return ['git', '-C', working_dir]
    return ['git']

def get_time_format():
    return time_format