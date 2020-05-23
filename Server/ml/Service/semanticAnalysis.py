import time
import couchdbService
import nltk
nltk.download('vader_lexicon')
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

def scenario_1_analyze():
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

    doc = dict()
    scenario1 = dict()
    for each in s1DataSet:
        texts = couchdbService.getTextsFromView(each["db_name"],each["view_name"])
        sentiment = nltk_analyze(texts)
        scenario1[each["area"]] = sentiment

    doc["scenario1"] = scenario1
    doc["created_at"] = time.asctime()

    server = couchdbService.server_connection()
    couchdbService.create_db(server, "scenario_analyze")
    db = couchdbService.get_db(server, "scenario_analyze")
    result = couchdbService.create_doc(db, doc)

    return result



def scenario_2_analyze() :
    s2DataSet = [
        {
			"area": "Adelaide",
			"db_name":"adelaide",
			"view_name":"twitter/jobrelated"
		},
		{
			"area": "Melbourne",
			"db_name":"melbourne_2018",
			"view_name":"twitter/jobrelated"
		}
    ]
    
    doc = dict()
    scenario2 = dict()
    for each in s2DataSet:
        texts = couchdbService.getTextsFromView(each["db_name"],each["view_name"])
        sentiment = nltk_analyze(texts)
        scenario2[each["area"]] = sentiment

    doc["scenario2"] = scenario2
    doc["created_at"] = time.asctime()

    server = couchdbService.server_connection()
    couchdbService.create_db(server, "scenario_analyze")
    db = couchdbService.get_db(server, "scenario_analyze")
    result = couchdbService.create_doc(db, doc)

    return result