#!/usr/bin/env python3
from python_lib import metadata, shared, timelog, visualconsole, dbook, git_timestore_calls as gtc
from python_lib.flask import app
import argparse, logging, re, importlib, json


def workon(args):
    shared.set_issue_number(args.issue)
    if args.time:
        if re.search(r'((\d){1,2})([h]|[H])', args.time):
            timelog.log_type('did', value=args.time)
        else:
            timelog.log_type('start', value=args.time)
    else:
        timelog.log_type('start')
        
def wrapup(args):
    if args.time:
        timelog.log_type('end', value=args.time)
    else:
        timelog.log_type('end')

def webreport(args):
    app.main()

def consolereport(args):
    visualconsole.main()

def dump(args):
    print(gtc.get_all_as_dict())

def push(args):
    gtc.push()

def fetch(args):
    gtc.fetch()

def global_settings(args):
    if args.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s')      
    
    if args.path:
        shared.set_working_dir(args.path)
    if args.quiet:
        shared.set_quiet_mode(True)

def argparser_setup():
    global args
    parser = argparse.ArgumentParser(prog='Git extension POC',)
    subparsers = parser.add_subparsers()

    #Global params
    parser.add_argument('-d', '--debug', action='store_true', help='Outputs debug data')
    parser.add_argument('-q', '--quiet', action='store_true', help='Removes console output from git commads')
    parser.add_argument('-C', '--path', help='Define a path', type=str)

    #workon subcommand
    parser_workon = subparsers.add_parser('workon', help='Start time logging')
    parser_workon.usage = 'git timereg workon [issue] [optional arguments]'
    parser_workon.add_argument('issue', type=int, help='Issue number timeregistration are to be referenced to')
    parser_workon.add_argument('-t', '--time', type=str, help='Define a custom time')
    parser_workon.set_defaults(func=workon)

    parser_wrapup = subparsers.add_parser('wrapup', help='Stop time logging')
    parser_wrapup.usage = 'git timereg wrapup [optional arguments]'
    parser_wrapup.add_argument('-t', '--time', type=str, help='Define a custom time')
    parser_wrapup.set_defaults(func=wrapup)

    parser_webreport = subparsers.add_parser('webreport', help='Launch report in web')
    parser_webreport.usage = 'git timereg webreport'
    parser_webreport.set_defaults(func=webreport)

    parser_consolereport = subparsers.add_parser('consolereport', help='Launch report in console')
    parser_consolereport.usage = 'git timereg consolereport'
    parser_consolereport.set_defaults(func=consolereport)

    parser_dump = subparsers.add_parser('dump', help='Show all stored timelogs in current directory')
    parser_dump.usage = 'git timereg dump'
    parser_dump.set_defaults(func=dump)

    parser_push = subparsers.add_parser('push', help='Push timelogs with automerge')
    parser_push.usage = 'git timereg push'
    parser_push.set_defaults(func=push)

    parser_fetch = subparsers.add_parser('fetch', help='Fetch timelogs with automerge')
    parser_fetch.usage = 'git timereg fetch'
    parser_fetch.set_defaults(func=fetch)

    args = parser.parse_args()

def main():
    importlib.reload(logging)
    importlib.reload(json)
    argparser_setup()

    global_settings(args)
    args.func(args)

if __name__ == '__main__':
    main()