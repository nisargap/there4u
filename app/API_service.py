from flask import Flask, render_template,jsonify, request
from pymongo import MongoClient
import random

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/getTweetId")
def get_password():
    client = MongoClient()
    DB = client["medHacks"]
    ourCollection = DB["sadTweets"]
    numItems = ourCollection.count()
    randomNum = random.randint(0,numItems)
    randomItem = ourCollection.find().skip(randomNum).limit(1)
    id_str = ""
    for doc in randomItem:
        id_str = doc["id_str"]
    return jsonify(id_str=id_str)



if __name__ == "__main__":

    app.run(host="0.0.0.0",port=80,debug=True)
