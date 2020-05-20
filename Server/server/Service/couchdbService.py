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

def queryViewCount(area, db_name,view_name):
    db = get_db(server, db_name)
    results=db.view(view_name)
    total_sum = db.__len__()
    return {"area":area,"total_sum":total_sum,"count":results.rows[0].value}

def queryGeojson(geo_name):
    json_results = {}
    if(geo_name.lower() == "melbourne"):
        json_results["rows"] = mel_geojson["features"]
    json_results["isSuccess"] = True
    return json_results