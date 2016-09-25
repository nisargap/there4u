import requests
import json
import urllib
def analyze_tone(text):
    username = 'a9d957a6-7329-44de-b478-cf9edb81cf7f'
    password = 'aax2OHyxfV7z'
    watsonUrl = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19&'
    headers = {"content-type": "text/plain"}
    try:
        r = requests.get(watsonUrl + urllib.urlencode({"text" : text}), auth=(username,password))
        emotions = r.json()["document_tone"]["tone_categories"][0]["tones"]
        
        result = max(emotions)
        
        if(result["score"] > 0.5):
            return result
        else:
            return False

    except:
        return False
