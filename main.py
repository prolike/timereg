#!/usr/bin/env python3
import sys
import os
import argparse


def main():
    global location, gitpath, variables

    arguments()

    location = os.getcwd()
    gitpath = find_git(location)
    variables = get_git_variables()

    if args.web:
        web()
    elif args.debug:
        debug()

def arguments():
    global args
    parser = argparse.ArgumentParser(prog="Git extension POC")
    parser.add_argument("-w", "--web", action="store_true", help="Opens the git repository in your browser.")
    parser.add_argument("-d", "--debug", action="store_true", help="Displays data from the %(prog)s script")
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

def debug():
    print("--------DEBUG--------")
    print("Run from:\t", location)
    print("Git path:\t", gitpath)
    print("Variables:\t", variables)
    print("---------------------")

if __name__ == "__main__":
    main()