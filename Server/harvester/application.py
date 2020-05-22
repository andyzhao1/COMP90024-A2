from flask import Flask, jsonify, abort, request, make_response, url_for
import time
import sys 
sys.path.append("Service") 
import twitterService
import collectRadius
from flask_httpauth import HTTPBasicAuth
import uuid
import threading

app = Flask(__name__, static_url_path = "")

# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# API
'''
### Name: startCollectTweet
### API: /stream/startCollectTweet
### Description: 
'''
@app.route('/stream/startCollectTweet', methods = ['POST'])
def startCollectTweet():
    if not request.json or not 'keyWords' in request.json or not 'databaseName' in request.json or not 'ConsumerKey' in request.json or not 'ConsumerSecret' in request.json or not 'AccessToken' in request.json or not 'TokenSecret' in request.json:
        abort(400)
    databaseName = request.json['databaseName']
    key_words = request.json['keyWords']
    consumer_key = request.json['ConsumerKey']
    consumer_secret = request.json['ConsumerSecret']
    access_token = request.json['AccessToken']
    access_token_secret = request.json['TokenSecret']

    return_info = twitterService.startStreamTweet(databaseName,key_words,consumer_key,consumer_secret,access_token,access_token_secret)
    return jsonify( return_info ), 200

'''
### Name: stopCollectTweet
### API: /stream/stopCollectTweet
### Description: 
'''
@app.route('/stream/stopCollectTweet', methods = ['POST'])
def stopCollectTweet():
    if not request.json or not 'stream_id' in request.json:
        abort(400)
    stream_id = request.json['stream_id']
    return_info = twitterService.stopStreamTweet(stream_id)
    return jsonify(return_info), 200


'''
### Name: queryStreamList
### API: '/stream/queryStreamList'
### Description: ''
'''
@app.route('/stream/queryStreamList', methods = ['GET'])
def queryStreamList():
    return_info = twitterService.queryStreamList()
    return jsonify(return_info), 200



'''''''''''''''''''''''''''''''''''''''''''''

'''''''''''''''''''''''''''''''''''''''''''''



'''
### Name: startCollectByRadius
### API: '/search/startCollectByRadius'
### Description: ''
'''
australia = '-29.1425,133.1389,2081km'
melbourne = '-37.7867,144.9082,100km'
sydney = '-33.8813,151.2128,100km'
brisbane = '-27.5394,153.1024,100km'
adelaide = '-34.9328,138.6444,100km'
perth = '-32.0379,115.8808,100km'

collecting_thread_information = []
collecting_thread_list = []
@app.route('/search/startCollectByRadius', methods = ['POST'])
def startCollectByRadius():
    if not request.json:
        abort(400)
    provinces = ""
    geocodes = []
    query = ""
    since = ""
    until = ""
    db_name = None
    if(request.json['db_name'] !=None):
        db_name = request.json['db_name']

    if(request.json['provinces'] !=None):
        provinces = request.json['provinces']

    if(request.json['geocodes'] !=None):
        geocodes = request.json['geocodes']

    if(request.json['since'] !=None):
        since = request.json['since']

    if(request.json['until']!=None):
        until = request.json['until']
    
    if(request.json['query'] !=None):
        query = request.json['query']

    #thread = threading.Thread(args=(query, provinces, geocodes, since, until))
    thread_id = str(uuid.uuid1())
    thread = collectRadius.StoppableThreadForCollectTweet(args=(query, provinces, geocodes, since, until,db_name,thread_id))
    thread_entity = {
        "thread_id":thread_id,
        "thread":thread,
        "information":{
            "provinces":provinces,
            "geocodes":geocodes,
            "since":since,
            "until":until,
            "query":query
        }
    }
    collecting_thread_list.append(thread_entity)

    thread_information = {
        "thread_id":thread_id,
        "information":{
            "provinces":provinces,
            "geocodes":geocodes,
            "since":since,
            "until":until,
            "query":query
        }
    }
    collecting_thread_information.append(thread_information)

    try:
        thread.start()
    except Exception as e:
        return jsonify( {"errorMessage":e, 'isSuccess': False } ), 200

    return jsonify( {"threadEntity":thread_information, 'isSuccess': True } ), 200

'''
### Name: stopCollectByRadius
### API: '/search/stopCollectByRadius'
### Description: ''
'''
@app.route('/search/stopCollectByRadius', methods = ['POST'])
def stopCollectByRadius():
    thread_ids = request.json['ids']
    for thread_id in thread_ids:
        thread_entity = None
        thread_information = None
        for i in range(len(collecting_thread_list)):
            if(collecting_thread_list[i]["thread_id"] == thread_id):
                thread_entity = collecting_thread_list.pop(i)
                thread_information = collecting_thread_information.pop(i)
                break

        if(thread_entity == None):
            return jsonify( {"errorMessage":"Thread not found", 'isSuccess': False } ), 200
        else:
            thread = thread_entity["thread"]
            try:
                thread.stop()
                thread.join()
                return jsonify( {"threadEntity":thread_information, 'isSuccess': False } ), 200
            except Exception as e:
                print(str(e))
                return jsonify( {"threadEntity":thread_information, 'isSuccess': True } ), 200
'''
### Name: collectByRadiusList
### API: '/search/queryCollectingThreadList'
### Description: ''
'''
@app.route('/search/queryCollectingThreadList', methods = ['GET'])
def collectByRadiusList():
    return jsonify( {"threadList":collecting_thread_information, 'isSuccess': True } ), 200


if __name__ == '__main__':
    app.run(port=5001,debug=True,threaded=True,host='0.0.0.0')

