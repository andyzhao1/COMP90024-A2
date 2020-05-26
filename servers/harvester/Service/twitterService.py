import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pip._vendor import requests
import couchdb
import json
import uuid
import GetOldTweets3 as got

stream_list = {}

class StdOutListenerForAU(StreamListener):

    def __init__(self, server, db_name,key_words,auth):
        self.server = server
        self.db_name = db_name
        self.key_words = key_words
        self.auth = auth

    def on_data(self,data):
        try:
            db = get_db(self.server, self.db_name)
            json_data=json.loads(data)
            json_data["_id"] = json_data['id_str']
            json_data["key_words"] = self.key_words
            doc = create_doc(db, json_data)
            print("Search By Location:"+str(doc["_id"]))
            return True

        except BaseException as e:
            print("Error on_data %s" % str(e))

        return True

    def on_error(self,status):
        print(status)
        if status == 420:
            return False

class TwitterStreamer():

    def __init__(self):
        pass

    def stream_tweets(self, server, db_name, key_words,consumer_key,consumer_secret,access_token,access_token_secret):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        listener = StdOutListenerForAU(server, db_name,key_words,auth)
        stream = Stream(auth, listener)
        stream_id = str(uuid.uuid1())
        stream_list[stream_id] = stream
        stream.filter(track=key_words, locations=locations, languages = ["en"], is_async=True)
        return {"stream":stream_id,"is_success":True}

#####################################################################################

def server_connection():
    try:
        server = couchdb.Server('http://COMP90024:COMP90024@172.26.132.195:5984/')
        print("CouchDB is connected: " + str(server) + "\n")
        return server

    except Exception as e:
        print(e)


########################################################################################################


def create_db(server, db_name):
    try:
        db = server.create(db_name)
        print("Database %s is created\n" % (db_name))
        return db
    except Exception as e:
        print(e)


def get_db(server, db_name):
    try:
        db = server[db_name]
        return db
    except Exception as e:
        print(e)


def create_doc(db, document):
    doc_id, doc_rev = db.save(document)
    doc = db[doc_id]
    return doc

server = server_connection()

#Search Area: Australia
locations=[109.59,-44.55,159.34,-11.05]


# ServiceImpl
def startStreamTweet(databaseName,keyWords,consumer_key,consumer_secret,access_token,access_token_secret):
    consumer_key = consumer_key
    consumer_secret = consumer_secret
    access_token = access_token
    access_token_secret = access_token_secret
    #Keywords for Search in Twitter: A list of strings
    twitter_streamer = TwitterStreamer()
    #(Server, Database Name, Keywords)
    return_info = twitter_streamer.stream_tweets(server, databaseName, keyWords,consumer_key,consumer_secret,access_token,access_token_secret)
    print(stream_list)
    return return_info

def stopStreamTweet(stream_id):
    print(stream_list.keys())
    if(stream_id in stream_list.keys()):
        stream = stream_list.pop(stream_id)
        stream.disconnect()
        return {'isSuccess': True, "stream_id": stream_id}
    else:
        return {'isSuccess': False, "error_message":"not found stream"}

def queryStreamList():
    stream_ids = []
    for each in stream_list.keys():
        stream_ids.append(each)
    print(stream_list)
    return {'isSuccess': True, "stream_list":stream_ids}
