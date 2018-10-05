from python_lib import metadata, shared, git_timestore_calls as gtc
from datetime import datetime
import subprocess


def main():
    username = shared.get_git_variables()['username']
    url = shared.get_git_variables()['url']
    split_days = metadata.split_on_days(gtc.get_all_as_dict())
    t_string = '\n'
    t_string += (username + ' worked on project ' + url.split('/')[4])
    t_string += ('\nurl: ' + url + '\n')
    t_string += table_print(split_days)
    print(t_string)

def table_print(value):
    r_string = ''
    for key in value:
        start_list, end_list = shared.listsplitter(value[key])    
        r_string += (datetime.strptime(key, '%Y-%m-%d').strftime('\n%A %Y-%m-%d') + '\n')
        r_string += (' Started   '.ljust(8) + 'Ended '.ljust(8) + '  Time worked\n')
        start_try = metadata.extract_time(start_list)
        end_try = metadata.extract_time(end_list)
        for start_time, end_time, stString, enString in zip(start_list, end_list, start_try, end_try):
            timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked([start_time], [end_time]))
            r_string += (' ' + metadata.visual_timestamp(stString).ljust(8) + '  ' + metadata.visual_timestamp(enString).ljust(8) + '  ' + metadata.remove_seconds_timestamp(timestr).ljust(8) + ' \n')
        timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list, end_list))
        r_string += (' Time worked today   ' + metadata.remove_seconds_timestamp(timestr).ljust(8) + ' \n')
    start_list_total, end_list_total = shared.listsplitter(metadata.order_days(gtc.get_all_as_dict()))
    timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list_total, end_list_total))
    r_string += ('\n Total time worked   ' + metadata.remove_seconds_timestamp(timestr).ljust(8) + ' \n')
    return r_string

if __name__ == '__main__':
    main()