import base64
import requests
import couchdb
import time
import sys
import threading
sys.path.append("../") 
import application

#####################################################################################

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

def print_time():
    now = time.localtime()
    print("Time: %04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))


#####################################################################################


#change this keys(consumer_key, consumer_secret)
consumer_key = "inmK8YNjwBxDdhhm8TisZMk3I"
consumer_secret = "QZlJDdczGXjoZf19KZmmP8DQ9Xh6cG4ZxtbXsyWC79ISHuI2jQ"


key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')


base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

auth_data = {
        'grant_type': 'client_credentials'
        }

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_resp.json()['access_token']

search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
        }


#####################################################################################


#[geocode: latitude,longitude,radius]
australia = '-29.1425,133.1389,2081km'
melbourne = '-37.7867,144.9082,100km'
sydney = '-33.8813,151.2128,100km'
brisbane = '-27.5394,153.1024,100km'
adelaide = '-34.9328,138.6444,100km'
perth = '-32.0379,115.8808,100km'


#change above Twitter account keys(consumer_key, consumer_secret)
#change above parameters only: query, since, until
server = server_connection()
# Class
class StoppableThreadForCollectTweet(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThreadForCollectTweet, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        query = self._args[0]
        provinces = self._args[1]
        geocodes = self._args[2]
        since = self._args[3]
        until = self._args[4]
        db_name = self._args[5]
        thread_id = self._args[6]

        for idx, province in enumerate(provinces):
            # initial start id
            since_id = 9999999999999999999999999999999999
            db = get_db(server, db_name[idx])
            print(db)
            if(db == None):
                db = create_db(server,db_name[idx])
            geocode = geocodes[idx]

            while True:
                if self.stopped():
                    return
                try:
                    search_params = {
                        'q': '{}'.format(query),
                        'geocode': '{}'.format(geocode),
                        'since': '{}'.format(since),  # only 7 days before
                        'until': '{}'.format(until),
                        'count': 100,  # max 100 with free api
                        'result_type': 'recent',  # mixed, recent, popular
                        'max_id': '{}'.format(str(since_id)),
                        'retryonratelimit': True
                    }

                    search_url = '{}1.1/search/tweets.json'.format(base_url)

                    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
                    tweet_data = search_resp.json()['statuses']

                    #print(search_resp)
                    #print(tweet_data)
                
                    if len(tweet_data) != 0:
                        for tweet in tweet_data:
                            print_time()
                            try:
                                since_id = tweet["id"]
                                tweet["_id"] = tweet["id_str"]
                                create_doc(db, tweet)

                                print("Tweet is collected [ {}_radius ]> {}\n".format(province, tweet["_id"]))

                            except Exception as e_db:
                                print(str(e_db)+"\n")

                        since_id = since_id - 1

                    else:
                        print("Tweets about the requested query does not exist\n")
                        for i in range(len(application.collecting_thread_list)):
                            if (application.collecting_thread_list[i].thread_id == thread_id):
                                application.collecting_thread_list.pop(i)
                                application.collecting_thread_information.pop(i)
                        break

                except Exception as e:
                    print_time()
                    print(e)

                    print("\nAPI reaches the rating limit, Sleep 15 min\n")
                    time.sleep(930)  # sleep 15min 30sec