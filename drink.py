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
            "glass_type": 1,
            "instructions": 1,
            "ingredients.ingredient": 1,
            "recognitions": 1,
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
            "glass_type": 1,
            "instructions": 1,
            "recognitions": 1,
            "_id": 0,
        }
    }
    ])


#pprint(drink_dict)

#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__, static_url_path = "/static")

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    #with open("index.html", 'r') as viz_file:
    #    return viz_file.read()
    db_ingredients = ["sweet vermouth", 
                        "gin", 
                        "Campari", 
                        "Cointreau", 
                        "Scotch"]
    return flask.render_template("index.html", db_ingredients = db_ingredients)

# Get an example and return it's score from the predictor model
@app.route("/subset", methods=["POST"])
def subset():
    """
    When A POST request with json data is made to this uri,
    Get the cocktails that can be made with the subset of ingredients
    """
    # Get decision score for our example that came with the request
 
    data = flask.request.json
    ingredients_list = data["ingredients"]

    drink_dict = mongo_query(ingredients_list)
    orig_length = len(drink_dict["result"])

    extended_drink_list = ingredients_list + ["fresh lime juice", "sugar"]
    extended_drink_dict = mongo_query(extended_drink_list)
    new_length = len(extended_drink_dict["result"])

    pprint(drink_dict)
    print >> sys.stderr, "old %i versus new %i" % (orig_length, new_length)
   
    #return flask.jsonify(extended_drink_dict)

  
    results = {"drinks": drink_dict, 
               "extended_drinks": extended_drink_dict}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

app.run(host='0.0.0.0', port=80, debug=True)
