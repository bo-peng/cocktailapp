from pprint import pprint
import pickle

with open("drinks_data.pkl", 'r') as picklefile: 
    drink_dict = pickle.load(picklefile)

pprint(drink_dict)
