#!/usr/bin/env python3
from python_lib import metadata, shared, timestore, timelog, visualhtml, visualconsole, dbook, git_timestore_calls as gtc
from python_lib.flask import app
import argparse
import logging
import re
import importlib


def main():
    arguments()
    importlib.reload(logging)

    if args.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s')      
    
    if args.path:
        shared.set_working_dir(args.path)
    if args.quiet:
        shared.set_quiet_mode(True)

    if args.logtimestart:
        if args.custom:
            if re.search(r'((\d){1,2})([h]|[H])', args.custom):
                timelog.log_type('did', value=args.custom)
            else:
                timelog.log_type('start', value=args.custom)
        else:
            timelog.log_type('start')
    if args.logtimeend:
        if args.custom:
            timelog.log_type('end', value=args.custom)
        else:
            timelog.log_type('end')
    if args.checktime:
        visualconsole.main()
        app.main()
    if args.test:
        shared.get_issue_number()
    
    if args.push:
        gtc.push()
    if args.fetch:
        gtc.fetch()

    if args.save:
        if args.commit:
            gtc.store(args.message, commit=args.commit)
        elif args.issue:
            gtc.store(args.message, issue=args.issue)
        elif args.issuecomment:
            gtc.store(args.message, issue_comment=args.issuecomment)

def arguments():
    global args
    parser = argparse.ArgumentParser(prog='Git extension POC')
    parser.add_argument('-d', '--debug', action='store_true', help='Outputs debug data')
    parser.add_argument('-C', '--path', help='Define a path', type=str)    
    parser.add_argument('-ls', '--logtimestart', action='store_true', help='Log the start time you used on the current issue')
    parser.add_argument('-le', '--logtimeend', action='store_true', help='Log the end time you used on the current issue')
    parser.add_argument('-c', '--custom', help='Define a custom time', type=str)
    parser.add_argument('-ct', '--checktime', action='store_true', help='Check how much time you used')
    
    parser.add_argument('-p', '--push', action='store_true', help='Push git notes')
    parser.add_argument('-f', '--fetch', action='store_true', help='Fetch git notes')
    parser.add_argument('-q', '--quiet', action='store_true', help='Removes console output from git commads')
    parser.add_argument('-t', '--test', action='store_true', help='Removes console output from git commads')


    parser.add_argument('-s', '--save', action='store_true', help='Saves in our custom objects')    
    parser.add_argument('-m', '--message', help='message', type=str, action='append')    
    parser.add_argument('--commit', help='commit', type=str)    
    parser.add_argument('-i', '--issue', help='issue', type=int)    
    parser.add_argument('-ic', '--issuecomment', help='issue comment', type=str)    


    args = parser.parse_args()

if __name__ == '__main__':
    main()