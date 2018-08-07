#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import logging as log


def main():
    global location, gitpath, variables

    arguments()

    location = os.getcwd()
    gitpath = find_git(location)
    variables = get_git_variables()

    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")        
    if args.web:
        web()

    ''' lOG ORDER
    log.debug("This is debug") #USE THIS FOR VERBOSE
    log.info("This is info")
    log.warning("This is warning")
    log.error("This is error")
    '''

def arguments():
    global args
    parser = argparse.ArgumentParser(prog="Git extension POC")
    parser.add_argument("-w", "--web", action="store_true", help="Opens the git repository in your browser.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Outputs verbose data")
    args = parser.parse_args()

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

def web():
    if variables["url"][:4] == "git@":
        link = "github.com/" + variables["url"].split(":")[-1][:-4]
    else:
        link = variables["url"][:-4]
    os.system("xdg-open " + link)
    log.debug("xdg-open " + link)

if __name__ == "__main__":
    main()