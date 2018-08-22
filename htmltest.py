from yattag import Doc, indent
from python_lib import metadata, shared, timestore
import subprocess


doc, tag, text = Doc().tagtext()

start_list, end_list = timestore.listsplitter(timestore.readfromfile())
username = shared.get_git_variables()['username']
url = shared.get_git_variables()['url']

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
                    url = 'https://github.com/prolike/timereg.git'
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
                        text('minutes worked')
                for start_time, end_time in zip(start_list, end_list):
                    with tag('tr'):
                        with tag('td'):
                            doc.attr(klass = 'left-text')
                            text(start_time)
                        with tag('td'):
                            doc.attr(klass = 'left-text')
                            text(end_time)
                        with tag('td'):
                            doc.attr(klass = 'center-text worked')
                            text(metadata.calc_time_worked([start_time], [end_time]))
            with tag('table'):
                with tag('tr'):
                    with tag('td'):
                        doc.attr(klass = 'right-left double-size-table')
                        text('Total minutes worked')
                    with tag('td'):
                        doc.attr(klass = 'center-text worked')
                        text(metadata.calc_time_worked(start_list, end_list))
with open('report/index.html', 'w') as f:
    f.write(indent(doc.getvalue()))
subprocess.call(['xdg-open', 'report/index.html'])