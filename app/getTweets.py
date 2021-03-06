from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import requests
import keys
from toneAnalyzer import analyze_tone
from pymongo import MongoClient

#Variables that contains the user credentials to access Twitter API 

count = 0

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        
        global count
        data = json.loads(data)
        try:        
            tone = analyze_tone(data["text"])
            id_str = data["id_str"]
#            name = data["user"]["name"]
            screen_name = data["user"]["screen_name"]
            creation_time = data['created_at']
        except:
            print (data)



 #       tones = tone['tones']



        if(tone):
            tone_name = tone["tone_name"]
            if(tone_name == "Sadness"):
                insertIntoDB(tone,id_str,creation_time);

        count += 1

        if count > 200:
            return False

        # merge stuff

        return True

    def on_error(self, status):
        print status


def insertIntoDB(tone,id_str,creation_time):
    client = MongoClient()
    db = client["medHacks"]
    collection = db["sadTweets"]

    collection.insert({ "tone":tone["score"],
                          "id_str":id_str,
                          "creation_time":creation_time
                      }
                     )                          



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['sad', 'angry', 'depressed', 'hate', 'sucks', ':(','depression','sick','crying','sorry','hurts','hurt'])

