# -*- coding: utf-8 -*-
"""
this is variation from tweet radius search script
this embeds suburb information of tweets harvested within specified radius
so that the tweet can be used in more location specified plots as well

@author: Kim
"""

import base64
import requests
import couchdb
import time
import sys

#####################################################################################

def server_connection():
    try:

        server = couchdb.Server('http://{}:{}@{}:{}/'.format(id, pw, ip, port))
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


def create_doc(db, document):
    doc_id, doc_rev = db.save(document)
    doc = db[doc_id]
    return doc

def print_time():
    now = time.localtime()
    print("Time: %04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))


def get_tweets(query, provinces, geocodes, since, until, server, base_url, search_headers):
    for idx, province in enumerate(provinces):
        # initial start id
        since_id = 9999999999999999999999999999999999

        db = get_db(server, "city_thirtyone_radius")
        geocode = geocodes[idx]

        while True:
            #print_time()
            #print("[ Send request to Twitter ]\n")

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
                            tweet['location'] = province
                            create_doc(db, tweet)

                            print("Tweet is collected [ city_thirtyone_radius ]> {}\n".format(tweet["_id"]))

                        except Exception as e_db:
                            print(str(e_db)+"\n")

                    since_id = since_id - 1

                else:
                    print("Tweets about the requested query does not exist\n")
                    break

            except Exception as e:
                print_time()
                print(e)

                print("\nAPI reaches the rating limit, Sleep 15 min\n")
                time.sleep(930)  # sleep 15min 30sec


#####################################################################################

server_id = sys.argv[1]
server_pw = sys.argv[2]
server_ip = sys.argv[3]
server_port = sys.argv[4]

consumer_key = sys.argv[5]
consumer_secret = sys.argv[6]

#####################################################################################


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

melbourne_city = "-37.8136,144.9631,4km"

City_of_Maroondah = '-37.8097,145.2591,3.9km'

City_of_Whitehorse = '-37.8286,145.1486,4km'

Yarra_Ranges_Shire = '-37.7451,145.7134,24.7km'

City_of_Bayside = '-37.9333,145.0163,3km'

Shire_of_Cardinia = '-38.1135,145.5802,17.9km'

City_of_Casey = '-38.1105,145.2922,10.08km'

City_of_Greater_Dandenong = '-38.0061,145.2038,5.7km'

City_of_Frankston= '-38.1404,145.1597,5.7km'

City_of_Glen_Eira = '-37.9035,145.0383,3.1km'

City_of_Kingston = '-37.9819,145.1045,4.77km'

City_of_Monash = "-37.9016,145.1155,4.5km"

Shire_of_Mornington_Peninsula = '-38.2854,145.0934,13.44km'

Towns_adjacent_to_Westernport = '-38.3563,145.2480,13.03km'

City_of_Stonnington = '-37.8596,145.0328,2.53km'

City_of_Brimbank = '-37.7595,144.8071,5.55km'

City_of_Hobsons_Bay = '-37.8361,144.8401,4km'

City_of_Maribyrnong = "-37.7951,144.8841,2.79km"

City_of_Melton = "-37.6882,144.6534,11.49km"

City_of_Moonee_Valley = "-37.7465,144.9061,3.28km"

City_of_Wyndham = '-37.9119,144.6534,11.64km'

City_of_Port_Phillip = '-37.8465,144.9667,2.27km'

City_of_Yarra = '-37.7979,144.9887,2.2km'

City_of_Banyule = '-37.7314,145.0824,3.96km'

City_of_Darebin = '-37.7278,145.0163,3.67km'

City_of_Hume = "-37.5987,144.8291,11.21km"

City_of_Moreland = "-37.7241,144.9502,3.57km"

Shire_of_Nillumbik = '-37.5977,145.2701,10.39km'

City_of_Whittlesea = "-37.5383,145.0934,11.06km"

City_of_Boroondara = '-37.8119,145.0714,3.87km'

City_of_Knox = '-37.8715,145.2480,5.34km'

City_of_Manningham = '-37.7669,145.1597,5.31km'

provinces = ['melbounre_city',
             'City_of_Maroondah',
            'City_of_Whitehorse',
            'Yarra_Ranges_Shire',
            'City_of_Bayside',
            'Shire_of_Cardinia',
            'City_of_Casey',
            'City_of_Greater_Dandenong',
            'City_of_Frankston',
            'City_of_Glen_Eira',
            'City_of_Kingston',
            'City_of_Monash',
            'Shire_of_Mornington_Peninsula',
            'Towns_adjacent_to_Westernport',
            'City_of_Stonnington',
            'City_of_Brimbank',
            'City_of_Hobsons_Bay',
            'City_of_Melton',
            'City_of_Moonee_Valley',
            'City_of_Wyndham',
            'City_of_Port_Phillip',
            'City_of_Yarra',
            'City_of_Banyule',
            'City_of_Darebin',
            'City_of_Hume',
            'City_of_Moreland',
            'Shire_of_Nillumbik',
            'City_of_Whittlesea',
            'City_of_Boroondara',
            'City_of_Knox',
            'City_of_Manningham']

geocodes = [melbourne_city,City_of_Maroondah,
            City_of_Whitehorse,Yarra_Ranges_Shire,City_of_Bayside,Shire_of_Cardinia,City_of_Casey,City_of_Greater_Dandenong,
            City_of_Frankston,City_of_Glen_Eira,City_of_Kingston,City_of_Monash,Shire_of_Mornington_Peninsula,Towns_adjacent_to_Westernport,
            City_of_Stonnington,City_of_Brimbank,City_of_Hobsons_Bay,City_of_Melton,City_of_Moonee_Valley,
            City_of_Wyndham,City_of_Port_Phillip,City_of_Yarra,City_of_Banyule,City_of_Darebin,City_of_Hume,City_of_Moreland,
            Shire_of_Nillumbik,City_of_Whittlesea,City_of_Boroondara,City_of_Knox,City_of_Manningham]


#####################################################################################
query = ""
since = "2020-05-16"
until = "2020-05-24"


#change above Twitter account keys(consumer_key, consumer_secret)
#change above parameters only: query, since, until
get_tweets(query, provinces, geocodes, since, until, server_connection(), base_url, search_headers)