from yattag import Doc, indent
from python_lib import metadata, shared, timestore
from datetime import datetime
import subprocess


doc, tag, text = Doc().tagtext()
username = shared.get_git_variables()['username']
url = shared.get_git_variables()['url']
split_days = metadata.split_on_days(timestore.readfromfile())

def main():
    username = shared.get_git_variables()['username']
    url = shared.get_git_variables()['url']
    split_days = metadata.split_on_days(timestore.readfromfile())

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('link'):
                doc.attr(rel = 'stylesheet', type = 'text/css', href = 'css/custom.css')
            with tag('link'):
                doc.attr(rel = 'stylesheet', type = 'text/css', href = 'css/table.css')
        with tag('body'):
            doc.attr(klass = 'center-site')
            with tag('div'):
                doc.attr(klass = 'center-text')
                with tag('h1'):
                    text('Work time table')
            with tag('div'):
                doc.attr(klass = 'info-section')
                with tag('ul'):
                    with tag('li'):
                        text('User ')
                        with tag('a'):
                            text(username)
                            doc.attr(href = 'https://www.github.com/' + username)
                    with tag('li'):
                        text('Working on ')
                        with tag('a'):
                            if url[:4] == 'git@':
                                url = url.split(':')[1]
                                text(url.split('/')[1][:-4])
                                doc.attr(href = 'https://www.github.com/' + url[:-4])
                            elif url[:4] == 'http':
                                urls = url.split('/')
                                text(urls[4][:-4])
                                doc.attr(href = url[:-4])
                            else:
                                text('project not found!')
                    with tag('li'):
                        with tag('input', id = 'tzTran'):
                            doc.attr(type = 'checkbox', checked = 'false')
                            text('Convert times to registred timezone')
            for key in split_days:
                with tag('p'):
                    text(datetime.strptime(key, '%Y-%m-%d').strftime('%A %d-%m-%Y'))
                    doc.attr(klass = 'datetime')
                with tag('div'):
                    doc.attr(klass = 'timetable')
                    with tag('table'):
                        with tag('tr'):
                            with tag('th'):
                                text('Started')
                            with tag('th'):
                                text('ended')
                            with tag('th'):
                                doc.attr(klass = 'worked')
                                text('Time worked')   
                        start_list, end_list = timestore.listsplitter(split_days[key])         
                        for start_time, end_time in zip(start_list, end_list):
                            with tag('tr'):
                                with tag('td'):
                                    doc.attr(klass = 'center-text timeconvert')
                                    text(metadata.extract_time(start_time))
                                with tag('td'):
                                    doc.attr(klass = 'center-text timeconvert')
                                    text(metadata.extract_time(end_time))
                                with tag('td'):
                                    doc.attr(klass = 'center-text worked')
                                    timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked([start_time], [end_time]))
                                    text(timestr)#+ '%.2f' % metadata.calc_time_worked([start_time], [end_time]))
                    with tag('table'):
                        with tag('tr'):
                            with tag('td'):
                                doc.attr(klass = 'right-left double-size-table')
                                text('Time worked this day',)
                            with tag('td'):
                                doc.attr(klass = 'center-text worked')
                                timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list, end_list))
                                text(timestr)
                                #text('%.2f' % metadata.calc_time_worked(start_list, end_list))
            with tag('div'):
                doc.attr(klass = 'totalwork')
                with tag('table'):
                    with tag('tr'):
                        with tag('td'):
                            doc.attr(klass = 'right-left double-size-table')
                            text('Total time worked')
                        with tag('td'):
                            doc.attr(klass = 'center-text worked')
                            start_list_total, end_list_total = timestore.listsplitter(metadata.order_days(timestore.readfromfile()))
                            timestr = metadata.seconds_to_timestamp(metadata.calc_time_worked(start_list_total, end_list_total))
                            text(timestr)#+ '%.2f' % metadata.calc_time_worked([start_time], [end_time]))
            with tag('script'):
                doc.attr(src = 'js/main.js')
        with tag('footer'):
            text('Open source project ')
            with tag('a'):
                text('github')
                doc.attr(href = 'https://github.com/prolike/timereg')
    with open(shared.get_gitpath()[:-5] + 'report/index.html', 'w') as f:
        f.write(indent(doc.getvalue()))
    subprocess.call(['xdg-open', shared.get_gitpath()[:-5] + 'report/index.html'])

if __name__ == '__main__':
    main()