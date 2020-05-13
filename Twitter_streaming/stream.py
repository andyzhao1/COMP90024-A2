from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import json

class myListener(StreamListener):

    def on_data(self, data):
        # When receiving data from twitter will call this method
        try:
            # print(data)
            db = get_db(server, "Twitter")  # get db
            data_json = json.loads(data)  # Decode the JSON from Twitter
            _id = data_json["id_str"]
            
            db.update([_id, data_json])  # insert the data into the couchdb into a collection(_id as id of couchDB docs)
			
        except Exception as e:
            print(e)

    def on_error(self, status):
        print("Error: " + str(status))

    def on_connect(self):
        print("You are now connected to the streaming API.")


def server_conn():
    try:
        server = couchdb.Server('http://COMP90024:COMP90024@172.26.131.52:5984/')
        return server
    except Exception as e:
        print(e)
		

def get_db(server, db_name):
    try:
        db = server[db_name]
        return db
    except Exception as e:
        print(e)


def update_doc(db, docs):
    db.update(docs)


# Twitter API key
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


server = server_conn()

# db = create_db(server, "Twiiter")
# Twiiter = get_db(server, 'Twiiter')


listener = myListener()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, listener)
stream.filter(track=['test'], is_async=True)
#res = stream.filter(track=['test'], is_async=True)
