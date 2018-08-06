import sys
import os
#import argparse


location = ""
gitpath = ""
variables = {}

def main():
    global location, gitpath, variables
    location = os.getcwd()
    gitpath = find_git(location)
    variables = get_git_variables()
    for arg in sys.argv:
        if arg == "-d" or arg == "--debug":
            debug()
        if arg == "-h" or arg == "--help":
            help()
        if arg == "-w" or arg == "--web":
            web(variables["url"].split(":")[-1])

def find_git(path):
    if os.path.isdir(path + "/.git/"):
        return path + "/.git/"
    else:
        strlist = path.split('/')
        newpath = "/".join(strlist[:-1])
        return find_git(newpath)

def get_git_variables():
    variables_temp = {}
    with open((gitpath + "HEAD"), 'r') as f:
        for line in f:
            variables_temp["branch"] = line.rstrip().split('/')[-1]
    with open(gitpath + "config", 'r') as f:
        for line in f:
            newline = line.strip().split(" = ")
            if newline[0] == "url":
                variables_temp["url"] =  newline[1]
    return variables_temp

def web(link):
    os.system("xdg-open github.com/" + link)

def help():
    print("---------------")
    print("HELP:")
    print("-d --debug       prints parameters")
    print("---------------\n")

def debug():
    print("---------------")
    print("DEBUG:")
    print("Run from:\t", location)
    print("Git path:\t", gitpath)
    print("Variables:\t", variables)
    print("---------------\n")

if __name__ == "__main__":
    main()