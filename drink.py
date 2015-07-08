#!/usr/bin/env python
import flask
from pprint import pprint
import pickle
import json

#---------- MODEL IN MEMORY ----------------#

with open("drinks_data.pkl", 'r') as picklefile: 
    drink_dict = pickle.load(picklefile)

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
    return json.dumps(drink_dict)

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
