#!/usr/bin/env python3
from python_lib import metadata, gitnotes, shared, timestore, timelog, visualhtml, visualconsole, dbook
import argparse
import logging
import re
import importlib


def main():
    arguments()
    importlib.reload(logging)

    if args.verbose:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s')      
    
    if args.path:
        shared.set_working_dir(args.path)
    if args.quiet:
        shared.set_quiet_mode(True)

    if args.logtimestart:
        logging.debug(f'Calling: args.logtimestart')
        if args.custom:
            if re.search(r'((\d){1,2})([h]|[H])', args.custom):
                timelog.log_type('did', value=args.custom)
            else:
                timelog.log_type('start', value=args.custom)
        else:
            timelog.log_type('start')
    if args.logtimeend:
        logging.debug(f'Calling: args.logtimeend')
        if args.custom:
            timelog.log_type('end', value=args.custom)
        else:
            timelog.log_type('end')
    if args.checktime:
        logging.debug(f'Calling: args.checktime')
        visualconsole.main()
        visualhtml.main()
    if args.dump:
        timestore.dump()    

    if args.push:
        gitnotes.push_notes()
    if args.fetch:
        gitnotes.fetch_notes()
    if args.test:
        dbook.test()



def arguments():
    global args
    parser = argparse.ArgumentParser(prog='Git extension POC')
    parser.add_argument('-v', '--verbose', action='store_true', help='Outputs verbose data')
    parser.add_argument('-C', '--path', help='Define a path', type=str)    
    parser.add_argument('-ls', '--logtimestart', action='store_true', help='Log the start time you used on the current issue')
    parser.add_argument('-le', '--logtimeend', action='store_true', help='Log the end time you used on the current issue')
    parser.add_argument('-c', '--custom', help='Define a custom time', type=str)
    parser.add_argument('-ct', '--checktime', action='store_true', help='Check how much time you used')
    parser.add_argument('-d', '--dump', action='store_true', help='Dump timelog on current commit')
    parser.add_argument('-p', '--push', action='store_true', help='Push git notes')
    parser.add_argument('-f', '--fetch', action='store_true', help='Fetch git notes')
    parser.add_argument('-q', '--quiet', action='store_true', help='Removes console output from git commads')
    parser.add_argument('-t', '--test', action='store_true', help='Removes console output from git commads')
    
    args = parser.parse_args()

if __name__ == '__main__':
    main()