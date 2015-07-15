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

def drinks_short_n(ingredients_list=[], n=1):
    return collection.aggregate(
        [
            { "$project": { "ingredients.ingredient": 1, 
                            "name": 1,
                            "site_id": 1,
                            "instructions": 1,
                            "recognitions": 1,
                            "glass_type": 1,
                            "inBOnly": 
                            { "$setDifference": ["$ingredients.ingredient", 
                                                 ingredients_list] 
                          }, 
                        } 
          },
            {
                "$match": { 
                    "inBOnly": {"$size": 1}
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
            },
            { "$limit" : 5 }
        ]
    )

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
    db_spirits = sorted(["gin",
                         "rum",
                         "tequila",
                         "vodka",
                         "Scotch",
                         "rye"], key=str.lower)
    db_liqueurs = sorted(["Cointreau",
                          "sweet vermouth",
                          "dry vermouth",
                          "Campari",
                          "Midori"], key=str.lower)
    db_mixers = ["tonic water",
                 "soda",
                 "ginger beer"]
    db_juices = ["orange juice",
                 "grapefruit juice",
                 "fresh lime juice"]
    db_bitters = ["Angustora bitters",
                  "orange bitters",
                  "Peychaud's bitters"]
    db_garnishes = ["lemon",
                    "lime",
                    "orange"]
    db_ingredients = [{"category": "Spirits",
                       "ingredients": db_spirits}, 
                      {"category": "Liqueurs",
                       "ingredients": db_liqueurs},
                      {"category": "Mixers",
                       "ingredients": db_mixers},
                      {"category": "Juices",
                       "ingredients": db_juices},                      
                      {"category": "Bitters",
                       "ingredients": db_bitters},                     
                      {"category": "Garnishes",
                       "ingredients": db_garnishes}]
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
    drink_dict_ids = [x["site_id"] for x in drink_dict["result"]]
    orig_length = len(drink_dict["result"])

    #extended_drink_list = ingredients_list + ["fresh lime juice"]
    extended_drink_dict = drinks_short_n(ingredients_list)

    # extended_drink_dict["result"] = [x for x in extended_drink_dict["result"] 
    #                                  if x["site_id"] not in drink_dict_ids]
    #import pdb; pdb.set_trace()
    new_length = len(extended_drink_dict["result"])

    pprint(drink_dict)
    print >> sys.stderr, "old %i versus new %i" % (orig_length, new_length)
   
    #return flask.jsonify(extended_drink_dict)

  
    results = {"drinks": drink_dict, 
               "extended_drinks": extended_drink_dict}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

app.run(host='0.0.0.0', port=80, debug=True)
