import time
import couchdbService
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def nltk_analyze(texts):
    sid = SentimentIntensityAnalyzer()
    sentiment = {"positive" : 0, "negative" : 0, "neutral" : 0}
    for text in texts :
        predict = sid.polarity_scores(text)
        predict.pop("compound")
        predict.pop("neu")

        if predict["pos"] == predict["neg"] :
            sentiment["neutral"] += 1
        else :
            _, key = max(zip(predict.values(), predict.keys()))
            if key == "pos" :
                sentiment["positive"] += 1
            if key == "neg" :
                sentiment["negative"] += 1
    return sentiment

def scenario_analyze(scenario) :
    s1DataSet = [
		{
			"area": "Melbourne",
			"db_name":"melbourne_radius",
			"view_name":"twitter/s1"
		},
		{
			"area": "Brisbane",
			"db_name":"brisbane_radius",
			"view_name":"twitter/s1"
		},
		{
			"area": "Sydney",
			"db_name":"sydney_radius",
			"view_name":"twitter/s1"
		},
        {
			"area": "Adelaide",
			"db_name":"adelaide",
			"view_name":"twitter/s1"
		},
        {
			"area": "Perth",
			"db_name":"perth_radius",
			"view_name":"twitter/s1"
		}
	]

    s2DataSet = [
		{
			"area": "Melbourne",
			"db_name":"melbourne_radius",
			"view_name":"twitter/jobrelated"
		},
		{
			"area": "Brisbane",
			"db_name":"brisbane_radius",
			"view_name":"twitter/jobrelated"
		},
		{
			"area": "Sydney",
			"db_name":"sydney_radius",
			"view_name":"twitter/jobrelated"
		},
        {
			"area": "Adelaide",
			"db_name":"adelaide",
			"view_name":"twitter/jobrelated"
		},
        {
			"area": "Perth",
			"db_name":"perth_radius",
			"view_name":"twitter/jobrelated"
		}
    ]

    doc = dict()
    if scenario == "scenario1" :
        dataSet = s1DataSet
        doc["description"] = "description"
    elif scenario == "scenario2" :
        dataSet = s2DataSet
        doc["description"] = "description"

    
    data = dict()
    for each in dataSet:
        if scenario == "scenario1" :
            texts = couchdbService.getTextsFromView_1(each["db_name"],each["view_name"])
        if scenario == "scenario2" :
            texts = couchdbService.getTextsFromView_2(each["db_name"],each["view_name"])
        sentiment = nltk_analyze(texts)
        data[each["area"]] = sentiment  
    doc["_id"] = scenario 
    doc["created_at"] = time.asctime()
    doc["data"] = data
    
    server = couchdbService.server_connection()
    couchdbService.create_db(server, "scenario_analyze")
    db = couchdbService.get_db(server, "scenario_analyze")
    try :
        db_doc = db[scenario]
        db_doc["created_at"] = doc["created_at"]
        db_doc["data"] = doc["data"]
        result = db.save(db_doc)
    except :
        result = couchdbService.create_doc(db, doc)

    return result

def scenario_4_analyze() :
    s4DataSet = [
		{
			"area": "Melbourne",
			"db_name":"melbourne_2016",
			"view_name":"twitter/unemployment"
		}
    ]
    
    doc = dict()
    data = dict()
    for each in s4DataSet:
        texts = couchdbService.getTextsFromView_4(each["db_name"],each["view_name"])
    #     sentiment = nltk_analyze(texts)
    #     data[each["area"]] = sentiment

    # doc["_id"] = "scenario4"
    # doc["description"] = "description"
    # doc["created_at"] = time.asctime()
    # doc["data"] = data

    # server = couchdbService.server_connection()
    # couchdbService.create_db(server, "scenario_analyze")
    # db = couchdbService.get_db(server, "scenario_analyze")
    # try :
    #     db_doc = db["scenario4"]
    #     db_doc["created_at"] = doc["created_at"]
    #     db_doc["data"] = doc["data"]
    #     result = db.save(db_doc)
    # except :
    #     result = couchdbService.create_doc(db, doc)


    # return result