import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pip._vendor import requests
import couchdb
import json
import uuid
import twint
import mmap
import json

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

def server_connection():
    try:
        server = couchdb.Server('http://COMP90024:COMP90024@172.26.132.195:5984/')
        print("CouchDB is connected: " + str(server) + "\n")
        return server

    except Exception as e:
        print(e)

def get_db(server, db_name):
    try:
        db = server[db_name]
        return db
    except Exception as e:
        print(e)

def isRayIntersectsSegment(poi,s_poi,e_poi): 
    if s_poi[1]==e_poi[1]: 
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]:
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]: 
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]: 
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]: 
        return False
    if s_poi[0]<poi[0] and e_poi[1]<poi[1]: 
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1])
    if xseg<poi[0]:
        return False
    return True 

def isPoiWithinPoly(poi,poly):
    sinsc=0 
    for epoly in poly: 
        for i in range(len(epoly)-1): 
            s_poi=epoly[i]
            e_poi=epoly[i+1]
            if isRayIntersectsSegment(poi,s_poi,e_poi):
                sinsc+=1 

    return True if sinsc%2==1 else  False


server = server_connection()
mel_geojson = read_json_file("JSON/mel_geojson.json")

# ServiceImpl
def queryView(db_name,view_name):
    db = get_db(server, db_name)
    results=db.view(view_name)
    json_results = {}
    rows = []
    for each in results.rows:
        if "study" in each["value"]["text"]:
            rows.append(each)
    print(len(rows))
    for each in rows:
        for section in mel_geojson["features"]:
            if(isPoiWithinPoly(each["value"]["coordinates"]["coordinates"],section["geometry"]["coordinates"][0])):
                each["value"]["geo"]=section["properties"]
    json_results["rows"] = rows
    json_results["isSuccess"] = True
    return json_results

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
def queryViewCount(area, db_name,view_name):
    db = get_db(server, db_name)
    results=db.view(view_name)
    total_sum = db.__len__()
    return {"area":area,"total_sum":total_sum,"count":results.rows[0].value}

def scenarioQuery(scenario):
    print(scenario)
    if(scenario == "s1"):
        s1GenerateResult = []
        db = get_db(server,"scenario_analyze")
        index = 0
        for each in db:
            index += 1
            if(index == 1):
                result = db[each]['scenario1']
        for each in result:
            s1GenerateResult.append({"area":each,"positive":result[each]["positive"],"negative":result[each]["negative"]})
        results = {"isSuccess":True,"data":s1GenerateResult}
    elif(scenario == "s2"):
        s2GenerateResult = []
        db_names = ["adelaide","brisbane_radius","melbourne_radius","perth_radius","sydney_radius"]
        for each in db_names:
            db = get_db(server,each)
        results = {"isSuccess":True,"data":s2GenerateResult}
    elif(scenario == "s3"):
        results = {"isSuccess":True,"data":s3GenerateResult}
    else:
        s3GenerateResult = []
        results = {"isSuccess":False,"error_message":"not found"}
    return results

def s1Generate(area, db_name,view_name):
    db = get_db(server, db_name)
    texts = db.view(view_name,reduce = False)
    positive = 0
    negative = 0
    equal = 0
    for each in texts:
        result = sid.polarity_scores(each.value)
        if(result["neg"]>result["pos"]):
            negative += 1
        elif(result["neg"]<result["pos"]):
            positive += 1
        else:
            equal += 1
    s1GenerateResult.append({"area":area,"positive":positive,"negative":negative,"equal":equal})

def s2Generate(area, db_name,view_name):
    db = get_db(server, db_name)
    texts = db.view(view_name,reduce = False)
    positive = 0
    negative = 0
    equal = 0
    for each in texts:
        result = sid.polarity_scores(each.value)
        if(result["neg"]>result["pos"]):
            negative += 1
        elif(result["neg"]<result["pos"]):
            positive += 1
        else:
            equal += 1
    s2GenerateResult.append({"area":area,"positive":positive,"negative":negative,"equal":equal})

def s3Generate(area, db_name,view_name):
    db = get_db(server, db_name)
    texts = db.view(view_name,reduce = False)
    positive = 0
    negative = 0
    equal = 0
    for each in texts:
        result = sid.polarity_scores(each.value)
        if(result["neg"]>result["pos"]):
            negative += 1
        elif(result["neg"]<result["pos"]):
            positive += 1
        else:
            equal += 1
    s2GenerateResult.append({"area":area,"positive":positive,"negative":negative,"equal":equal})  

def queryGeojson(geo_name):
    json_results = {}
    if(geo_name.lower() == "melbourne"):
        json_results = mel_geojson
    print(mel_geojson)
    return json_results