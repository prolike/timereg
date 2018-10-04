from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api, request
from python_lib import shared, metadata, timelog, git_timestore_calls as gtc
from datetime import datetime
import json, time


app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    git_var = shared.get_git_variables()
    clean_dict = gtc.get_all_as_dict()
    # print(clean_dict)
    order = metadata.order_days(clean_dict)
    split_days = metadata.split_on_days(clean_dict)
    start, end = shared.listsplitter(clean_dict)
    data = {}
    data['username'] = git_var['username']
    data['total_time_worked'] = metadata.calc_time_worked(start, end)
    data['split_days'] = split_days
    data['ordered'] = order
    jsonTest = json.dumps(data)
    #print(json.dumps(data, indent=4, sort_keys=True))
    return render_template('body.html', username=git_var['username'],
                           url=git_var['url'], split=jsonTest)

@app.route('/api/test')
def api_test():
    try:
        return jsonify({'state': 'Succes!'})
    except:
        return jsonify({'state': 'Failed!'})

class addtime(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        try:
            json_data = request.get_json(force=True)
            issue = json_data['issue']
            start_time = json_data['start_time']
            end_time = json_data['end_time']
            username = json_data['username']
            data = {}
            data['info'] = {'issue': issue, 'start_time': start_time,
                            'end_time': end_time, 'username': username}
            shared.set_issue_number(issue)
            tz = metadata.get_tz_info()
            start_time = metadata.convert_from_js(start_time, tz)
            end_time = metadata.convert_from_js(end_time, tz)
            start_time += ':00' + tz
            end_time += ':00' + tz
            path = shared.get_gitpath()
            issuenumber = shared.get_issue_number()

            note_dict_start = {}
            note_dict_start['storage'] = {'repo': path, 'issue': issuenumber}
            note_dict_start['content'] = {'user': username, 'state': 'start', 'timestamp': start_time}
            note_dict_end = {}
            note_dict_end['storage'] = {'repo': path, 'issue': issuenumber}
            note_dict_end['content'] = {'user': username, 'state': 'end', 'timestamp': end_time}     
            gtc.store_json(str(note_dict_start).replace('\'', '"'))
            gtc.store_json(str(note_dict_end).replace('\'', '"'))

            newdata = {}
            newdata['split_days'] = metadata.split_on_days(gtc.get_all_as_dict())
            return jsonify(status="Succes", data=data, newdata=newdata)
        except:
            json_data = request.get_json(force=True)
            start_time = json_data['start_time']
            return jsonify(status="Failed", data=json_data)

class edittime(Resource):

    def post(self):
        try:
            json_data = request.get_json(force=True)
            username = json_data['username']
            start_time = json_data['start_time']
            end_time = json_data['end_time']
            def_start_time = json_data['def_start_time']
            def_end_time = json_data['def_end_time']
            start_issue_hash = json_data['startih']
            start_line_hash = json_data['startlh']
            end_issue_hash = json_data['endih']
            end_line_hash = json_data['endlh']
            tz = metadata.get_tz_info()
            start_time = metadata.convert_from_js(start_time, tz)
            end_time = metadata.convert_from_js(end_time, tz)
            if datetime.strptime(start_time, '%Y-%m-%dT%H:%M') < datetime.strptime(end_time, '%Y-%m-%dT%H:%M'):
                if start_time != def_start_time[:-8]:
                    time = start_time[11:]
                    datestamp = start_time[:10]
                    month = datestamp[5:-3]
                    date = datestamp[-2:]
                    hour = time[:2]
                    minute = time[-2:]
                    start_newObj = {'user': username, 'state': 'start', 'timestamp': metadata.time(chour=hour, cminute=minute, cday=date, cmonth=month)}
                    gtc.store(commit=start_issue_hash, remove=start_line_hash, entry=start_newObj)
                if end_time != def_end_time[:-8]:
                    time = end_time[11:]
                    datestamp = end_time[:10]
                    month = datestamp[5:-3]
                    date = datestamp[-2:]
                    hour = time[:2]
                    minute = time[-2:]
                    end_newObj = {'user': username, 'state': 'end', 'timestamp': metadata.time(chour=hour, cminute=minute, cday=date, cmonth=month)}
                    gtc.store(commit=end_issue_hash, remove=end_line_hash, entry=end_newObj)
            data = {}
            data['user'] = username
            newdata = {}
            newdata['split_days'] = metadata.split_on_days(gtc.get_all_as_dict())
            return jsonify(status="Succes", data=data, newdata=newdata)
        except:
            data = {}
            return jsonify(status="Failed", data=json_data)

class getweek(Resource):
    def get(self):
        return metadata.match_week(gtc.get_all_as_dict(), 'this')

class getall(Resource):
    def get(self):
        newdata = {}
        newdata['split_days'] = metadata.split_on_days(gtc.get_all_as_dict())
        return jsonify(newdata=newdata)

api.add_resource(edittime, '/edittime')
api.add_resource(addtime, '/addtime')
api.add_resource(getweek, '/getweek')
api.add_resource(getall, '/getall')

def main():
    # Remove debug=True to disable auto reload on code change + on release!
    app.run(debug=True, host='0.0.0.0', port=5000)
