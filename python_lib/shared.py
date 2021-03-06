import os, subprocess, logging, re, hashlib
from . import settings

issue_number = 0
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
    logging.debug(f'shared.set_working_dir({path})')
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
    logging.debug(f'shared.path_routing({path})')
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
    logging.debug(f'shared.path_up_level({cwd}, {path})')
    if path[:3] == '../':
        return path_up_level('/'.join(cwd.split('/')[:-1]), path.split('/',1)[1])
    else:
        return cwd + '/' + path

def get_work_dir():
    logging.debug(f'shared.get_work_dir()')
    return working_dir

def get_gitpath():
    logging.debug(f'shared.get_gitpath()')
    global gitpath
    if gitpath == '':
        gitpath = find_git(working_dir)

    return gitpath    

def set_quiet_mode(mode):
    logging.debug(f'shared.set_quiet_mode({mode})')
    global quiet_mode
    quiet_mode = mode

def git_suffix():
    '''
    Send a list of suffixes in this case --quiet to mute commands if quiet mode is turned on

    Return:
        list: Returns a list of suffixes to git commands
    '''
    logging.debug(f'shared.git_suffix()')
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
    logging.debug(f'shared.find_git({path})')
    if os.path.isdir(path + '/.git/'):
        return path + '/.git/'
    else:
        strlist = path.split('/')
        newpath = '/'.join(strlist[:-1])
        return find_git(newpath)

def get_git_variables():
    logging.debug(f'shared.get_git_variables()')
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
    logging.debug(f'shared.get_git_variables()')
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
    variables_temp['url'] = _get_http_link(url.stdout.decode('utf-8').rstrip())
    variables_temp['username'] = username.stdout.decode('utf-8').rstrip()
    return variables_temp

def _get_http_link(url):
    logging.debug(f'shared._get_http_link({url})')
    if url[:4] == 'git@':
        url = url.split(':')[1]
        return 'https://www.github.com/' + url[:-4]
    elif url[:4] == 'http':
        url = url.split('/')
        return 'https://www.github.com/' + url[3] + '/' + url[4][:-4]
    elif url[:1] == '/':
        return url

def git_prefix():
    '''
    Makes the prefix -C param if needed to use all git commands in another folder than the cwd

    Retrun:
        list: Returns a list with the prefixes for git calls 
    '''
    logging.debug(f'shared.git_prefix()')
    if os.getcwd() != working_dir:
        return ['git', '-C', working_dir]
    return ['git']

def get_time_format():
    logging.debug(f'shared.get_time_format()')
    return time_format

def get_issue_number():
    global issue_number
    if issue_number is 0:
        with open(get_gitpath() + 'HEAD') as f:
            line = f.readline()
            try:
                temp = re.search(r'((heads\/)\d+(-))', line).group(0)
                temp = temp[6:-1]
                issue_number = int(temp)
            except:
                logging.error('Unable to extract issue number form current branch')
    return issue_number

def set_issue_number(number):
    global issue_number
    issue_number = number

def generate_git_sha1_issue(number):
    url = (get_git_variables()['url'] + '/issue/' + str(number))
    content = ('blob ' + str(len(url)) + '\0' + url)
    return sha1_gen(content)

def sha1_gen(content):
    sha1 = hashlib.sha1()
    sha1.update(str.encode(content))
    return sha1.hexdigest()

def sha1_gen_dict(content):
    content = str(content)
    sha1 = hashlib.sha1()
    sha1.update(str.encode(content))
    return sha1.hexdigest()

def listsplitter(los):
    '''
    Take whatever content we have in tempfile and sorts it in our
    2 different tags so we can play nice with them.

    Args:
        param1(list): los - los or list of strings is a as the name says
        a list of string with our meta data.

    Return:
        list: start_list - A list with all the meta tags start
        list: end_list - A list with all the meta tags end
    '''
    logging.debug(f'timestore.listsplitter({los})')
    start_list = []
    end_list = []
    for string in los:
        if type(string) is dict:
            metatag = string['state']
            if metatag == 'start':
                start_list.append(string)
            elif metatag == 'end':
                end_list.append(string)
        if type(string) is str:
            for test in los[string]:
                metatag = los[string][test]['state']
                if metatag == 'start':
                    start_list.append(los[string][test])
                elif metatag == 'end':
                    end_list.append(los[string][test])
    return start_list, end_list

def autopush():
    return str_to_bool(settings.get_setting('autopush'))

def str_to_bool(s):
    s = s.lower()
    if s == 'true':
         return True
    elif s == 'false':
         return False
    else:
         raise ValueError