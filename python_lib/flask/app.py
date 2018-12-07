from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api, request
from python_lib import shared, metadata, timelog, git_timestore_calls as gtc
from datetime import datetime
import json
import time


app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('body.html')


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
            issuenumber = shared.get_issue_number()

            note_dict = {}
            note_dict = {'user': shared.get_git_variables()['username'], 'timestamp_start': start_time,
                         'timestamp_end': end_time, 'issue': issuenumber}
            gtc.store(target=[shared.get_git_variables()[
                      'username'], datetime.now().year, datetime.now().month], content=note_dict)
            newdata = {}
            newdata['split_days'] = metadata.split_on_days(gtc.get_all_by_path([shared.get_git_variables()['username'], datetime.now(
            ).year, datetime.now().month]))
            return jsonify(status="Succes", newdata=newdata)
        except:
            print('CRASH!')
            newdata['split_days'] = metadata.split_on_days(gtc.get_all_by_path([shared.get_git_variables()['username'], datetime.now(
            ).year, datetime.now().month]))
            return jsonify(status="Failed", data=newdata)


class edittime(Resource):
    def post(self):
        try:
            json_data = request.get_json(force=True)
            sha1 = json_data['sha1']
            newissue = json_data['issue']
            timestamp_start = json_data['start_time']
            timestamp_end = json_data['end_time']
            tz = metadata.get_tz_info()
            og = gtc.get_all_by_path([shared.get_git_variables(
            )['username'], datetime.now().year, datetime.now().month])[sha1]
            try:
                issue = og['issue']
            except:
                issue = None
            try:
                if int(issue) != int(newissue):
                    issue = newissue
            except:
                issue = newissue
            timestamp_start = metadata.convert_from_js(timestamp_start, tz)
            timestamp_end = metadata.convert_from_js(timestamp_end, tz)
            if datetime.strptime(timestamp_start, '%Y-%m-%dT%H:%M') <= datetime.strptime(timestamp_end, '%Y-%m-%dT%H:%M'):
                time = timestamp_start[11:]
                datestamp = timestamp_start[:10]
                month = datestamp[5:-3]
                date = datestamp[-2:]
                hour = time[:2]
                minute = time[-2:]
                timestamp_start = metadata.time(
                    chour=hour, cminute=minute, cday=date, cmonth=month)
                time = timestamp_end[11:]
                datestamp = timestamp_end[:10]
                month = datestamp[5:-3]
                date = datestamp[-2:]
                hour = time[:2]
                minute = time[-2:]
                timestamp_end = metadata.time(
                    chour=hour, cminute=minute, cday=date, cmonth=month)
            
            gtc.store(target=[shared.get_git_variables()['username'], datetime.now().year, datetime.now().month], remove=sha1, content={
                      'timestamp_end': timestamp_end, 'timestamp_start': timestamp_start, 'issue': issue, 'user': shared.get_git_variables()['username']})

            newdata = {}
            newdata['split_days'] = metadata.split_on_days(gtc.get_all_by_path([shared.get_git_variables()['username'], datetime.now(
            ).year, datetime.now().month]))
            return jsonify(status="Succes", newdata=newdata)
        except:
            print('CRASH!')
            newdata = {}
            newdata['split_days'] = metadata.split_on_days(gtc.get_all_by_path([shared.get_git_variables()['username'], datetime.now(
            ).year, datetime.now().month]))
            return jsonify(status="Failed", data=newdata)


# class getweek(Resource):
    # def get(self):
        # return metadata.match_week(gtc.get_all_as_dict(), 'this')


class getall(Resource):
    def get(self):
        newdata = {}
        newdata['split_days'] = metadata.split_on_days(gtc.get_all_by_path([shared.get_git_variables()['username'], datetime.now(
        ).year, datetime.now().month]))
        return jsonify(newdata=newdata)


class delete(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        sha1 = json_data['sha1']
        gtc.store(target=[shared.get_git_variables()['username'],
                          datetime.now().year, datetime.now().month], remove=sha1)
        newdata = {}
        newdata['split_days'] = metadata.split_on_days(gtc.get_all_by_path([shared.get_git_variables()['username'], datetime.now(
        ).year, datetime.now().month]))
        return jsonify(newdata=newdata)


api.add_resource(edittime, '/edittime')
api.add_resource(addtime, '/addtime')
api.add_resource(getall, '/getall')
api.add_resource(delete, '/delete')
# api.add_resource(getweek, '/getweek')


def main():
    # Remove debug=True to disable auto reload on code change + on release!
    app.run(debug=True, host='0.0.0.0', port=5000)
