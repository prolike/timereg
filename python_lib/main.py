from datetime import datetime
from time import mktime as mktime
import sys
import os
import re
import webbrowser
import subprocess
import logging

def main():
    global location, gitpath, variables

    location = os.getcwd()
    gitpath = find_git(location)
    variables = get_git_variables() 

    ''' lOG ORDER
    logging.debug("This is debug") #USE THIS FOR VERBOSE
    logging.info("This is info")
    logging.warning("This is warning")
    logging.error("This is error")
    '''

def find_git(path):
    if os.path.isdir(path + "/.git/"):
        return path + "/.git/"
    else:
        strlist = path.split('/')
        newpath = "/".join(strlist[:-1])
        return find_git(newpath)

def time(**kwargs):
    chour = kwargs.get('chour', None)
    cminute = kwargs.get('cminute', None)
    format = "%d-%m-%Y/%H:%M"
    now = datetime.now()
    if chour is not None:
        now = now.replace(hour=int(chour))
    if cminute is not None:
        now = now.replace(minute=int(cminute))
    return now.strftime(format)

def log(state, **kwargs):
    note_string = '[' + variables['username'] + '][' + state + ']'
    value = kwargs.get('value', None)
    try:
        if re.search(r"([01]\d|2[0-3]):[0-5]\d", value):
            chour = value.split(":")[0]
            cminute = value.split(":")[1]
            note_string += time(chour=chour, cminute=cminute)
            print(note_string)
        elif re.search(r"([01]\d|2[0-3])?[0-5]\d", value):
            if len(value) is 3:
                note_string += time(cminute=value[-2:], chour=value[:1])
            else:
                note_string += time(cminute=value[-2:], chour=value[:2])
            print(note_string)
        else:
            note_string += time()
            print(note_string)
    except:
        note_string += time()
        print(note_string)
    return 1

def get_git_variables():
    variables_temp = {}
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD", "--"], stdout=subprocess.PIPE)
    url = subprocess.run(["git", "config", "--get", "remote.origin.url"], stdout=subprocess.PIPE)
    username = subprocess.run(['git', 'config', 'github.user'], stdout=subprocess.PIPE)
    variables_temp["branch"] = branch.stdout.decode("utf-8").rstrip()[:-3]
    variables_temp["url"] = url.stdout.decode("utf-8").rstrip()
    variables_temp['username'] = username.stdout.decode('utf-8').rstrip()
    return variables_temp

def calc_time_worked(started, ended):
    fmt = "%d-%m-%Y/%H:%M"
    total_min_worked = 0

    logging.debug('Cleaning metadata')
    name = get_clean_name_meta_data(started)
    clean_start = get_clean_time_meta_data(started)
    clean_end = get_clean_time_meta_data(ended)
    
    #print(name, clean_start, clean_end)
    logging.debug("Checking for missing timestamps")
    if len(started) > len(ended):
        logging.warning("You are missing some timestamps!")
    logging.debug('Calculating time worked')
    for start_time, end_time in zip(clean_start, clean_end):
        d1 = mktime(datetime.strptime(start_time, fmt).timetuple())
        d2 = mktime(datetime.strptime(end_time, fmt).timetuple())
        total_min_worked += (int(d2-d1) / 60) #Prints time worken in min
    return total_min_worked

def get_clean_time_meta_data(meta_data):
    cleaned_data = []
    for data in meta_data:
        cleaned_data.append(re.search(r'((\d{2}-){2}(\d{4}))/(([01]\d|2[0-3]):[0-5]\d)', data).group(0)) #Very brittle!
    return cleaned_data

def get_clean_name_meta_data(meta_data):
    return re.findall(r'\[(.+?)\]', meta_data[0])[0]

def clean_meta_list(dirtylist):
    index_remove = []
    clean_list = dirtylist
    for idx, element in enumerate(dirtylist):
        if cleaner(element) is True:
            index_remove.append(idx)
    index_remove.reverse()
    for idx in index_remove:
        del clean_list[idx]
    return clean_list

def cleaner(data_element):
    format = "%d-%m-%Y/%H:%M"
    metatag = re.findall(r'\[(.*?)\]', data_element)
    try:
        if metatag[1] != "start" and metatag[1] != "end":
            return True
        if len(metatag[0]) == 0 or len(metatag[0]) > 39:
            return True    
        date = re.search(r'((\d{2}-){2}(\d{4}))/(([01]\d|2[0-3]):[0-5]\d)', data_element).group(0)
        datetime.strptime(date, format)
    except:
        return True
    return False

def web():
    if variables["url"][:4] == "git@":
        link = "github.com/" + variables["url"].split(":")[-1][:-4]
    else:
        link = variables["url"][:-4]
    logging.debug("webbrowser.open " + link)
    webbrowser.open(link, new=0, autoraise=True)

if __name__ == "__main__":
    main()