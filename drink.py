#!/usr/bin/env python
import sys
import flask
from pprint import pprint
import pickle
import json

from pymongo import MongoClient

#---------- OPEN DATABASE CONNECTION----------------#
client = MongoClient()
db = client.cocktailapp
collection = db.cocktaildb

def mongo_query(ingredients_list=[]):
    return collection.aggregate([{
        "$project": {
            "name": 1,
            "site_id": 1,
            "ingredients.ingredient": 1,
            "AisSubset": {
                "$setIsSubset": ["$ingredients.ingredient", ingredients_list]
            },
            "num_ingredients": {"$size": "$ingredients"}
        }
    },
    {
        "$match": {
            "AisSubset": True,
            "num_ingredients": {"$gt": 0}
        }
         
    },
    {
        "$project": {
            "name": 1,
            "site_id": 1,
            "ingredients.ingredient":1,
            "_id": 0,
        }
    }
    ])


#pprint(drink_dict)

#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    #with open("index.html", 'r') as viz_file:
    #     return viz_file.read()
    ingredients_list = ["sweet vermouth", 
                        "gin", 
                        "Campari", 
                        "Cointreau", 
                        "Scotch"]


    drink_dict = mongo_query(ingredients_list)
    orig_length = len(drink_dict["result"])

    extended_drink_list = ingredients_list + ["fresh lime juice", "sugar"]
    extended_drink_dict = mongo_query(extended_drink_list)
    new_length = len(extended_drink_dict["result"])

    pprint(drink_dict)
    print >> sys.stderr, "old %i versus new %i" % (orig_length, new_length)
   
    return flask.jsonify(extended_drink_dict)

# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.matrix(data["example"])
    score = PREDICTOR.predict_proba(x)
    # Put the result in a nice dict so we can send it as json
    results = {"score": score[0,1]}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

app.run(host='0.0.0.0', port=80, debug=True)
