from python_lib import metadata, shared, timestore
from datetime import datetime
import subprocess


def main():
    username = shared.get_git_variables()['username']
    url = shared.get_git_variables()['url']
    split_days = metadata.split_on_days(timestore.readfromfile())
    print(username, 'worked on project ' + url.split('/')[4])
    print('url:', url)
    print('\nSadly its not possible to edit dates with these graphics'
    + '\ninstead use the commands or the HTML layout')
    table_print(split_days)

def table_print(value):
    for key in value:
        start_list, end_list = timestore.listsplitter(value[key])    
        print(datetime.strptime(key, '%Y-%m-%d').strftime('\n%A %Y-%m-%d'))
        print('---------------------------------------------------')
        print('| Started       | Ended         | Time worked     |')
        print('---------------------------------------------------')
        for start_time, end_time in zip(start_list, end_list):
            stString = metadata.extract_time(start_time)
            enString = metadata.extract_time(end_time)
            timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked([start_time], [end_time]))
            print('| ' + stString.ljust(13) + ' | ' + enString.ljust(13) + ' | ' + timestr.ljust(15) + ' |')
            print('---------------------------------------------------')
        timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list, end_list))
        print('| Time worked today             | ' + timestr.ljust(15) + ' |')
        print('---------------------------------------------------')
    start_list_total, end_list_total = timestore.listsplitter(metadata.order_days(timestore.readfromfile()))
    timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list_total, end_list_total))
    print('---------------------------------------------------')
    print('| Total time worked             | ' + timestr.ljust(15) + ' |')
    print('---------------------------------------------------')

if __name__ == '__main__':
    main()