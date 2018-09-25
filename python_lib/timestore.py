from python_lib import shared, metadata
import os
import re
import logging


def createfolder():
    '''
    Makes .time folder if it doesnt exist already.
    '''
    logging.debug(f'timestore.createfolder()')
    path = shared.get_gitpath()[:-5]
    if not os.path.exists(path + '.time'):
        try:
            os.makedirs(path + '.time')
        except:
            logging.error('Failed to make folder')

def writetofile(time_list):
    '''
    Writes to a tempfile in the .time folder, to save what the user has worked in hours

    Args:
        param1(list): time_list - Takes list with strings that its supposed to write to file
    '''
    logging.debug(f'timestore.writetofile({time_list})')
    createfolder()
    with open(shared.get_gitpath()[:-5] + '.time/tempfile', 'a') as f:
        for string in time_list:
            f.write(string + '\n')

def readfromfile():
    '''
    Collects all the lines in tempfile and puts them in a list

    Return:
        list: Returns a list with meta data thats been temp saved.
    '''
    logging.debug(f'timestore.readfromfile')
    path = shared.get_gitpath()[:-5]
    if not os.path.exists(path + '.time/tempfile'):
        pass
    else:
        times = []
        with open(path + '.time/tempfile', 'r') as f:
            for line in f:
                times.append(line.split('\n')[0])
            return times 
    return []

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
