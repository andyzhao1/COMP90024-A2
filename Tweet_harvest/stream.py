# -*- coding: utf-8 -*-
"""
Tweet streaming collecting tweets to couch DB

@author: Kim
"""


import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pip._vendor import requests
import couchdb
import json

class StdOutListener(StreamListener):

    def __init__(self, server, db_name):
        self.server = server
        self.db_name = db_name

    def on_data(self,data):
        try:
            print(data)
            db = get_db(self.server, self.db_name)

            doc = create_doc(db, json.loads(data))

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

    def stream_tweets(self, server, db_name):
        listener = StdOutListener(server, db_name)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)

        stream.filter( locations=locations )

#####################################################################################

def server_connection():
    try:
        server = couchdb.Server('http://COMP90024:COMP90024@172.26.131.52:5984/')
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




if __name__ == "__main__":
    server = server_connection()

    #Twitter API Credentials
    consumer_key = "FdOWknR0kOmopUKitybdP3S4D"
    consumer_secret = "mWVveTcyGjKAAFhmDEsF6meZYJnhYGPSRyfA9eBnLC4ZALDOlI"
    access_token =  "1260739078699356160-lrNNtNsTJqXXybZP0hqGDPjWGThEDM"
    access_token_secret = "ljYtgxDEoc7ZHXVzNAVGjTK3Z1pdEAyfSyUFWknEHOQyW"


    #Search Area: Australia
    locations=[109.59,-44.55,159.34,-11.05]

    #Keywords for Search in Twitter: A list of strings
    #keywords=['study','education','homeschooling','school','homework','assignment']

    twitter_streamer = TwitterStreamer()

    #(Server, Database Name, Keywords)
    twitter_streamer.stream_tweets(server, "tweet_keywords")