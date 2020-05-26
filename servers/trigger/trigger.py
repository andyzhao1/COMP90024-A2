import requests
import time
import json
from datetime import timedelta, datetime
from flask import Flask, jsonify, abort, request, make_response, url_for
import time
import sys 
from flask_httpauth import HTTPBasicAuth
import uuid
import threading
import mmap

app = Flask(__name__, static_url_path = "")

# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            map = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
            data=map.read().decode('utf-8')
            json_data=json.loads(data)
            f.close()
        return json_data
    except Exception as e:
        print(e)

def save_json_file(file_name,data):
    json_str = json.dumps(data)
    with open(file_name,"w") as json_file:
        json_file.write(json_str)
    print("save finished")

def auto_allocate_tasks_harvester():
    while True:
        tasks = read_json_file("tasks.json")
        db_names = tasks["db_names"]
        provinces = tasks["provinces"]
        geocodes = tasks["geocodes"]
        query = tasks["query"]
        since = (datetime.today() + timedelta(-1)).strftime('%Y-%m-%d')
        until = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        for i in range(len(db_names)):
            data = {
                "db_name" : db_names[i],
                "provinces" : provinces[i],
                "geocodes" : geocodes[i],
                "since" : since,
                "until" : until,
                "query" : query[i]
            }
            url='http://172.26.132.195:10000/harvester/search/startCollectByRadius'
            print(url)
            print(data)
            payload= data
            r = requests.post(url, json=payload)
            print (r.status_code)
        time.sleep(86400)

def auto_allocate_tasks_ml():
    while True:
        methods = ['/scenario/1/analyzeSemantic','/scenario/2/analyzeSemantic','/scenario/4/analyzeSemantic']
        for each in methods:
            url='http://172.26.132.195:10000/ml' + str(each)
            print(url)
            r = requests.post(url, data=None)
            print (r.status_code)
        time.sleep(3600)

@app.route('/tasks/add', methods = ['POST'])
def add():
    if not request.json or not 'db_names' in request.json or not 'provinces' in request.json or not 'geocodes' in request.json or not 'query' in request.json:
        abort(400)
    task_id = str(uuid.uuid1())
    db_names = request.json['db_names']
    provinces = request.json['provinces']
    geocodes = request.json['geocodes']
    query = request.json['query']

    tasks = read_json_file("tasks.json")

    tasks['ids'].append(task_id)
    tasks['db_names'].append(db_names)
    tasks['provinces'].append(provinces)
    tasks['geocodes'].append(geocodes)
    tasks['query'].append(query)

    print(tasks)
    save_json_file('tasks.json',tasks)
    return jsonify( {"message":"task is created", 'isSuccess': True } ), 200

@app.route('/tasks/delete', methods = ['POST'])
def delete():
    if not request.json or not 'ids' in request.json:
        abort(400)
    tasks = read_json_file("tasks.json")
    
    ids = request.json["ids"]
    
    new_tasks = {
        "ids":[],
        "db_names":[],
        "provinces":[],
        "geocodes":[],
        "query":[]
    }
    
    for index in range(len(tasks['ids'])):
        if(tasks['ids'][index] not in ids):
            print(tasks['ids'][index])
            new_tasks["ids"].append(tasks['ids'][index])
            new_tasks["db_names"].append(tasks['db_names'][index])
            new_tasks["provinces"].append(tasks['provinces'][index])
            new_tasks["geocodes"].append(tasks['geocodes'][index])
            new_tasks["query"].append(tasks['query'][index])


    save_json_file('tasks.json',new_tasks)
    return jsonify( {"message":'task is deleted', 'isSuccess': True } ), 200

@app.route('/tasks/query', methods = ['GET'])
def query():
    tasks = read_json_file("tasks.json")
    data = []
    for i in range(len(tasks['ids'])):
        data.append({"id":tasks["ids"][i],"db_names":tasks["db_names"][i],"provinces":tasks["provinces"][i],"geocodes":tasks["geocodes"][i],"query":tasks["query"][i]})
    return jsonify( {"tasks":data, 'isSuccess': True } ), 200

if __name__ == '__main__':
    threading.Thread(target=auto_allocate_tasks_harvester,args=()).start()
    threading.Thread(target=auto_allocate_tasks_ml,args=()).start()
    app.run(port=5003,debug=True,threaded=True,host='0.0.0.0')