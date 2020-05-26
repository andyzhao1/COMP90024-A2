import couchdb
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

def create_db(server, db_name):
    try:
        db = server.create(db_name)
        print("Database %s is created\n" % (db_name))
        return db
    except Exception as e:
        print(e)
               
def create_doc(db, document):
    doc_id, doc_rev = db.save(document)
    doc = db[doc_id]
    return doc

# ServiceImpl
def getTextsFromView_1(db_name,view_name):
    server = server_connection()
    db = get_db(server,db_name)
    view = db.view(view_name,reduce = False)
    texts = []
    for each in view:
        texts.append(each.value)
    return texts

def getTextsFromView_2(db_name,view_name):
    server = server_connection()
    db = get_db(server,db_name)
    view = db.view(view_name,reduce = False)
    texts = []
    for each in view:
        texts.append(each.value['text'])
    return texts

def getTextsFromView_4(db_name,view_name):
    server = server_connection()
    db = get_db(server,db_name)
    view = db.view(view_name,reduce = False)
    texts = []

    sid = SentimentIntensityAnalyzer()
    for each in view:
        # texts.append(each.value['text'])
        doc_id = each.id
        db_doc = db[doc_id]
        
        predict = sid.polarity_scores(each.value['text'])
        predict.pop("compound")
        predict.pop("neu")
        if predict["pos"] == predict["neg"] :
            sentiment = "neutral"
        else :
            _, key = max(zip(predict.values(), predict.keys()))
            if key == "pos" :
                sentiment = "positive"
            if key == "neg" :
                sentiment = "negative"
    
        db_doc["semantic_analysis"] = sentiment
        result = db.save(db_doc)

    return texts


