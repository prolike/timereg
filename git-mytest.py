#!/usr/bin/env python3
from python_lib import metadata, gitnotes, shared
import argparse
import logging

def main():
    arguments()

    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")      
    
    if args.path:
        shared.set_working_dir(args.path)

    if args.logtimestart:
        if args.custom:
            metadata.log("start", value=args.custom)
        else:    
            metadata.log("start")
    if args.logtimeend:        
        if args.custom:
            metadata.log("end", value=args.custom)
        else:    
            metadata.log("end")
    if args.checktime:
        starts = ['[davidcarl][start]08-08-2018/12:34', '[davidcarl][start]08-08-2018/15:00']
        ended = ['[davidcarl][end]08-08-2018/13:34', '[davidcarl][end]08-08-2018/15:30']
        logging.debug('calling: calc_time_worked')
        metadata.calc_time_worked(starts, ended) #Testing purposes
    if args.push:
        gitnotes.push_notes()
    if args.fetch:
        gitnotes.fetch_notes()



def arguments():
    global args
    parser = argparse.ArgumentParser(prog="Git extension POC")
    parser.add_argument("-v", "--verbose", action="store_true", help="Outputs verbose data")
    parser.add_argument("-C", "--path", help="Define a path", type=str)    
    parser.add_argument("-ls", "--logtimestart", action="store_true", help="Log the start time you used on the current issue")
    parser.add_argument("-le", "--logtimeend", action="store_true", help="Log the end time you used on the current issue")
    parser.add_argument("-c", "--custom", help="Define a custom time", type=str)
    parser.add_argument('-ct', '--checktime', action="store_true", help='Check how much time you used')
    parser.add_argument("-p", "--push", action="store_true", help="Push git notes")
    parser.add_argument("-f", "--fetch", action="store_true", help="Fetch git notes")
    
    args = parser.parse_args()

if __name__ == "__main__":
    main()