from flask import Flask, jsonify, abort, request, make_response, url_for
import time
import sys 
sys.path.append("Service")
import semanticAnalysis
from flask_httpauth import HTTPBasicAuth
import uuid
import threading
import random

app = Flask(__name__, static_url_path = "")

# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# Class
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            time.sleep(1)


# API

'''
### Name: semantic analyze for scenario 1
### API: '/scenario/1/analyzeSemantic'
### Description: ''
'''
@app.route('/scenario/1/analyzeSemantic', methods = ['POST'])
def s1_analyzeSemantic():
    if request.json:
        abort(400)
    result = semanticAnalysis.scenario_analyze(scenario="scenario1")
    return jsonify( result ), 201

'''
### Name: semantic analyze for scenario 2
### API: '/scenario/2/analyzeSemantic'
### Description: ''
'''
@app.route('/scenario/2/analyzeSemantic', methods = ['POST'])
def s2_analyzeSemantic():
    if request.json:
        abort(400)
    result = semanticAnalysis.scenario_analyze(scenario="scenario2")
    return jsonify( result ), 201

'''
### Name: semantic analyze for scenario 4
### API: '/scenario/4/analyzeSemantic'
### Description: ''
'''
@app.route('/scenario/4/analyzeSemantic', methods = ['POST'])
def s4_analyzeSemantic():
    if request.json:
        abort(400)
    result = semanticAnalysis.scenario_4_analyze()
    return jsonify( result ), 201

if __name__ == '__main__':
    app.run(port=5002,debug=True,threaded=True,host='0.0.0.0')

