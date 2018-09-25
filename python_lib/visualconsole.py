from python_lib import metadata, shared, timestore, git_timestore_calls as gtc
from datetime import datetime
import subprocess


def main():
    username = shared.get_git_variables()['username']
    url = shared.get_git_variables()['url']
    split_days = metadata.split_on_days(gtc.get_all_as_dict())
    t_string = '\n'
    t_string += (username + ' worked on project ' + url.split('/')[4])
    t_string += ('\nurl: ' + url)
    t_string += ('\n\nSadly its not possible to edit dates with these graphics\ninstead use the commands or the HTML layout\n')
    t_string += table_print(split_days)
    print(t_string)

def table_print(value):
    r_string = ''
    for key in value:
        start_list, end_list = timestore.listsplitter(value[key])    
        r_string += (datetime.strptime(key, '%Y-%m-%d').strftime('\n%A %Y-%m-%d') + '\n')
        r_string += ('---------------------------------------------------\n')
        r_string += ('| Started       | Ended         | Time worked     |\n')
        r_string += ('---------------------------------------------------\n')
        start_try = metadata.extract_time(start_list)
        end_try = metadata.extract_time(end_list)
        for start_time, end_time, stString, enString in zip(start_list, end_list, start_try, end_try):
            timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked([start_time], [end_time]))
            r_string += ('| ' + stString.ljust(13) + ' | ' + enString.ljust(13) + ' | ' + timestr.ljust(15) + ' |\n')
            r_string += ('---------------------------------------------------\n')
        timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list, end_list))
        r_string += ('| Time worked today             | ' + timestr.ljust(15) + ' |\n')
        r_string += ('---------------------------------------------------\n')
    start_list_total, end_list_total = timestore.listsplitter(metadata.order_days(gtc.get_all_as_dict()))
    timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list_total, end_list_total))
    r_string += ('---------------------------------------------------\n')
    r_string += ('| Total time worked             | ' + timestr.ljust(15) + ' |\n')
    r_string += ('---------------------------------------------------\n')
    return r_string

if __name__ == '__main__':
    main()