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

def isRayIntersectsSegment(poi,s_poi,e_poi): #[x,y] [lng,lat]
    #输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    if s_poi[1]==e_poi[1]: #排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]: #线段在射线上边
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]: #线段在射线下边
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]: #交点为下端点，对应spoint
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]: #交点为下端点，对应epoint
        return False
    if s_poi[0]<poi[0] and e_poi[1]<poi[1]: #线段在射线左边
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1]) #求交
    if xseg<poi[0]: #交点在射线起点的左侧
        return False
    return True  #排除上述情况之后

def isPoiWithinPoly(poi,poly):
    #输入：点，多边形三维数组
    #poly=[[[x1,y1],[x2,y2],……,[xn,yn],[x1,y1]],[[w1,t1],……[wk,tk]]] 三维数组

    #可以先判断点是否在外包矩形内 
    #if not isPoiWithinBox(poi,mbr=[[0,0],[180,90]]): return False
    #但算最小外包矩形本身需要循环边，会造成开销，本处略去
    sinsc=0 #交点个数
    for epoly in poly: #循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
        for i in range(len(epoly)-1): #[0,len-1]
            s_poi=epoly[i]
            e_poi=epoly[i+1]
            if isRayIntersectsSegment(poi,s_poi,e_poi):
                sinsc+=1 #有交点就加1

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

'''
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

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
'''


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
        result = db['scenario1']['data']
        for each in result:
            s1GenerateResult.append({"area":each,"positive":result[each]["positive"],"negative":result[each]["negative"]})
        results = {"isSuccess":True,"data":s1GenerateResult}
    elif(scenario == "s2"):
        s2GenerateResult = []
        db = get_db(server,"scenario_analyze")
        result = db['scenario2']['data']
        area_list = ["Sydney","Melbourne","Brisbane","Adelaide","Perth"]
        for each in area_list:
            s2GenerateResult.append({"area":each,"positive":result[each]["positive"],"negative":result[each]["negative"]})
        results = {"isSuccess":True,"data":s2GenerateResult}
    elif(scenario == "s3"):
        s3GenerateResult = []
        results = {"isSuccess":True,"data":s3GenerateResult}
    return results

sectionJobCount = {}
def jobRelatedTweetsDistribution():
    db = get_db(server, "melbourne_2016")
    view = db.view("twitter/unemployment",reduce = False)
    if (len(sectionJobCount) == 0):
        for each in view:
            print(each.key)
            if(each['value']['geo'] != None and each['value']['place'] != None and each['value']['place']['name'] == "Melbourne"):
                for section in mel_geojson["features"]:
                    each['value']['geo']['coordinates'][0],each['value']['geo']['coordinates'][1] = each['value']['geo']['coordinates'][1],each['value']['geo']['coordinates'][0]
                    if(isPoiWithinPoly(each['value']['geo']['coordinates'],section["geometry"]["coordinates"][0])):
                        if(section["properties"]["SA2_MAIN16"] in sectionJobCount.keys()):
                            if(each['value']["semantic_analysis"] == "positive"):
                                sectionJobCount[section["properties"]["SA2_MAIN16"]]["positive"] += 1
                            else:
                                sectionJobCount[section["properties"]["SA2_MAIN16"]]["negative"] += 1
                            break
                        else:
                            if(each['value']["semantic_analysis"] == "positive"):
                                sectionJobCount[section["properties"]["SA2_MAIN16"]] = {"name":section["properties"]["SA2_NAME16"],"positive":1,"negative":0}
                            else:
                                sectionJobCount[section["properties"]["SA2_MAIN16"]] = {"name":section["properties"]["SA2_NAME16"],"positive":0,"negative":1} 
                            break
    else:
        return {"isSuccess":True,"data":sectionJobCount}
    return {"isSuccess":True,"data":sectionJobCount}

def queryGeojson(geo_name):
    json_results = {}
    if(geo_name.lower() == "melbourne"):
        json_results = mel_geojson
    print(mel_geojson)
    return json_results