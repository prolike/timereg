from flask import Flask, render_template, jsonify
from python_lib import shared, metadata, timestore
import os, json


app = Flask(__name__)

@app.route('/')
def index():
    git_var = shared.get_git_variables()
    split_days = metadata.split_on_days(timestore.readfromfile())
    start, end = timestore.listsplitter(timestore.readfromfile())
    #result = ['1','2','3','4','5']
    data = {}
    data['start'] = start
    data['end'] = end
    data['total_time_worked'] = metadata.seconds_to_timestamp(metadata.calc_time_worked(start, end))
    data['split_days'] = split_days
    jsonTest = json.dumps(data)
    print(json.dumps(data, indent=4, sort_keys=True))
    return render_template('test.html', username = git_var['username'],\
                           url = git_var['url'], split=jsonTest)

@app.route('/api/test')
def api_test():
    try:
        os.makedirs('testfolder')
        return jsonify({'state': 'Succes!'})
    except:
        return jsonify({'state': 'Failed!'})

def main():
    app.run(debug=True) #Remove debug=True to disable auto reload on code change + on release!