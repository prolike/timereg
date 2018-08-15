from python_lib import shared
import os
import re


def createfolder():
    if not os.path.exists(shared.get_gitpath()[:-5] + '.time'):
        try:
            os.makedirs(shared.get_gitpath()[:-5] + '.time')
        except:
            print('Failed to make folder')

def writetofile(time_list):
    createfolder()
    f = open(shared.get_gitpath()[:-5] + '.time/tempfile', 'a')
    for string in time_list:
        f.write(string + '\n')

def printfile():
    if not os.path.exists(shared.get_gitpath()[:-5] + '.time/tempfile'):
        print('The file does not exist!')
    else:
        f = open(shared.get_gitpath()[:-5] + '.time/tempfile', 'r')
        for idx, line in enumerate(f):
            print(idx, line.split('\n')[0])

def readfromfile():
    if not os.path.exists(shared.get_gitpath()[:-5] + '.time/tempfile'):
        print('The file does not exist!')
    else:
        times = []
        f = open(shared.get_gitpath()[:-5] + '.time/tempfile', 'r')
        for line in f:
            times.append(line.split('\n')[0])
        return times 

def listsplitter(los):
    start_list = []
    end_list = []
    for string in los:
        metatag = re.findall(r'\[(.*?)\]', string)
        if metatag[1] == 'start':
            start_list.append(string)
        elif metatag[1] == 'end':
            end_list.append(string)
    return start_list, end_list