from flask import Flask, jsonify, abort, request, make_response, url_for
import time
import sys 
sys.path.append("Service") 
import couchdbService
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
### Name: test
### API: '/test/count'
### Description: ''
'''
@app.route('/test/count/query', methods = ['POST'])
def testCountQuery():
    if not request.json or not 'db_views' in request.json:
        abort(400)
    db_views = request.json['db_views']
    data = []
    for each in db_views:
        area = each['area']
        #db_name = each['db_name']
        #view_name = each['view_name']
        data.append({"area":area,"total_sum":random.randint(1000000,1500000),"count":random.randint(96000,240000)})
    result = {"data":data,"isSuccess":True}
    return jsonify( result ), 200


'''
### Name: scenario for tweets count
### API: '/count/query'
### Description: ''
'''
@app.route('/count/query', methods = ['POST'])
def countQuery():
    if not request.json or not 'db_views' in request.json:
        abort(400)
    db_views = request.json['db_views']
    data = []
    for each in db_views:
        area = each['area']
        db_name = each['db_name']
        view_name = each['view_name']
        data.append(couchdbService.queryViewCount(area,db_name,view_name))
    result = {"data":data,"isSuccess":True}
    return jsonify( result ), 200


'''
### Name: scenario for tweets count
### API: '/count/query'
### Description: ''
'''
@app.route('/scenario/query', methods = ['POST'])
def scenarioQuery():
    if not request.json or not 'scenario' in request.json:
        abort(400)
    scenario = request.json['scenario']
    result = couchdbService.scenarioQuery(scenario)
    return jsonify( result ), 200
#################################################################
'''
### Name: helloWorld
### API: '/test/helloWorld'
### Description: ''
'''
@app.route('/test/helloWorld', methods = ['GET'])
def helloWorld():
    return jsonify( {"isSuccess":True} ), 200

'''
### Name: queryView
### API: '/todo/api/v1.0/queryView'
### Description: ''
'''
@app.route('/todo/api/v1.0/queryView', methods = ['POST'])
def queryView():
    if not request.json or not 'db_name' in request.json or not 'view_name' in request.json:
        abort(400)
    db_name = request.json['db_name']
    view_name = request.json['view_name']
    result = couchdbService.queryView(db_name,view_name)
    return jsonify( result ), 200
'''

### Name: queryGeojson
### API: '/todo/api/v1.0/queryGeojson'
### Description: ''
'''
@app.route('/todo/api/v1.0/queryGeojson', methods = ['POST'])
def queryGeo():
    if not request.json or not 'geo_name' in request.json:
        abort(400)
    geo_name = request.json['geo_name']
    result = couchdbService.queryGeojson(geo_name)
    return jsonify( result ), 200

'''

### Name: queryGeojson1
### API: '/todo/api/v1.0/queryGeojson1'
### Description: ''
'''
@app.route('/todo/api/v1.0/queryGeojson1', methods = ['GET'])
def queryGeo1():
    result = {"isSuccess":True,"data":[{"city_name":"Yarra Valley","postive":5720,"negative":8847}]}
    return jsonify( result ), 200

if __name__ == '__main__':
    s1DataSet = [
		{
			"area": "Melbourne",
			"db_name":"melbourne_radius",
			"view_name":"twitter/coordinates"
		},
		{
			"area": "Brisbane",
			"db_name":"brisbane_radius",
			"view_name":"twitter/coordinates"
		},
		{
			"area": "Sydney",
			"db_name":"sydney_radius",
			"view_name":"twitter/coordinates"
		}
	]

    s2DataSet = [
		{
			"area": "Melbourne",
			"db_name":"melbourne_radius",
			"view_name":"twitter/coordinates"
		},
		{
			"area": "Brisbane",
			"db_name":"brisbane_radius",
			"view_name":"twitter/coordinates"
		},
		{
			"area": "Sydney",
			"db_name":"sydney_radius",
			"view_name":"twitter/coordinates"
		}
	]

    s3DataSet = [
		{
			"area": "Melbourne",
			"db_name":"melbourne_radius",
			"view_name":"twitter/coordinates"
		},
		{
			"area": "Brisbane",
			"db_name":"brisbane_radius",
			"view_name":"twitter/coordinates"
		},
		{
			"area": "Sydney",
			"db_name":"sydney_radius",
			"view_name":"twitter/coordinates"
		}
	]
    for each in s1DataSet:
        area = each["area"]
        db_name = each["db_name"]
        view_name = each["view_name"]
        couchdbService.s1Generate(area,db_name,view_name)
    
    app.run(port=5000,debug=True,threaded=True,host='0.0.0.0')

