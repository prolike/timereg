from python_lib import shared
import os
import re


def createfolder():
    '''
    Makes .time folder if it doesnt exist already.
    '''
    if not os.path.exists(shared.get_gitpath()[:-5] + '.time'):
        try:
            os.makedirs(shared.get_gitpath()[:-5] + '.time')
        except:
            print('Failed to make folder')

def writetofile(time_list):
    '''
    Writes to a tempfile in the .time folder, to save what the user has worked in hours

    Args:
        param1(list): time_list - Takes list with strings that its supposed to write to file
    '''
    createfolder()
    f = open(shared.get_gitpath()[:-5] + '.time/tempfile', 'a')
    for string in time_list:
        f.write(string + '\n')

def printfile():
    '''
    Prints the files content in the cli
    '''
    if not os.path.exists(shared.get_gitpath()[:-5] + '.time/tempfile'):
        pass
    else:
        f = open(shared.get_gitpath()[:-5] + '.time/tempfile', 'r')
        for idx, line in enumerate(f):
            print(idx, line.split('\n')[0])

def readfromfile():
    '''
    Collects all the lines in tempfile and puts them in a list

    Return:
        list: Returns a list with meta data thats been temp saved.
    '''
    if not os.path.exists(shared.get_gitpath()[:-5] + '.time/tempfile'):
        pass
    else:
        times = []
        f = open(shared.get_gitpath()[:-5] + '.time/tempfile', 'r')
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
    start_list = []
    end_list = []
    for string in los:
        metatag = re.findall(r'\[(.*?)\]', string)
        if metatag[1] == 'start':
            start_list.append(string)
        elif metatag[1] == 'end':
            end_list.append(string)
    return start_list, end_list