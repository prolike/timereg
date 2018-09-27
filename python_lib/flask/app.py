from flask import Flask, render_template, jsonify
from python_lib import shared, metadata, git_timestore_calls as gtc
import json


app = Flask(__name__)

@app.route('/')
def index():
    git_var = shared.get_git_variables()
    clean_dict = gtc.get_all_as_dict()
    order = metadata.order_days(clean_dict)
    split_days = metadata.split_on_days(clean_dict)
    start, end = shared.listsplitter(clean_dict)
    data = {}
    data['total_time_worked'] = metadata.calc_time_worked(start, end)
    data['split_days'] = split_days
    data['ordered'] = order
    jsonTest = json.dumps(data)
    #print(json.dumps(data, indent=4, sort_keys=True))
    return render_template('test.html', username = git_var['username'],\
                           url = git_var['url'], split=jsonTest)

@app.route('/api/test')
def api_test():
    try:
        return jsonify({'state': 'Succes!'})
    except:
        return jsonify({'state': 'Failed!'})

def main():
    app.run(debug=True) #Remove debug=True to disable auto reload on code change + on release!