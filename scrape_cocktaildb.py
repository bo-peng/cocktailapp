#!/usr/bin/env python
import sys
import requests
import re
import pickle

from bs4 import BeautifulSoup
from pymongo import MongoClient
from pprint import pprint


def get_soup(drink_id_number, base_url = "http://cocktaildb.com"):
    url = base_url + "/recipe_detail?id=" + str(drink_id_number)
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    return soup



def get_ingredients(soup):
    drink_ingredients=[]
    for recipeMeasure in soup.find_all("div", {"class": "recipeMeasure"}):
        ingredient = " or ".join([a.text for a in recipeMeasure.find_all("a")])
        measure = recipeMeasure.text.split(ingredient)[0].strip()

        # alternate measure units
        alt_units_span = recipeMeasure.find("span", {"class": "recipeAltUnits"})
        if alt_units_span:
            alt_units = alt_units_span.text 
        else:
            alt_units = None

        drink_ingredients.append({
            "ingredient": ingredient, 
            "rel_measure": measure,
            "alt_units": alt_units,
        })

       
      
    return drink_ingredients

def get_instructions_and_glass(soup, glass_type=None):
    instructions=[]
    for recipeDirection in soup.find_all("div", {"class": "recipeDirection"}):
        instruction_text = recipeDirection.text
        instructions.append(instruction_text)

        potential_link_element = recipeDirection.find("a")
        if potential_link_element:
            if "barwr_detail" in potential_link_element["href"]:
                glass_type = recipeDirection.find("a").text
        
    return instructions, glass_type

def open_mongo_connection():
    client = MongoClient()
    db = client.cocktailapp
    collection = db.cocktaildb
    return collection
    
if __name__ == '__main__':

    collection = open_mongo_connection()

    master_drink_list = []
    #recipes go from 1 to 4758
    for i in range(1, 4758+1):
    #for i in range(3555, 4759):

        # for some reason this one page is missing
        if i == 3550:
            continue

        if i % 50 == 0:
            print >> sys.stderr, "just got %i %s" % (i, drink_name)
  
        soup = get_soup(i)
        drink_name = soup.find(id="wellTitle").find("h2").text
        ingredients = get_ingredients(soup)
        instructions, glass_type = get_instructions_and_glass(soup)

        drink_document = {"name": drink_name,
                          "ingredients": ingredients,
                          "instructions": instructions,
                          "glass_type": glass_type,
                          "site_id": i,
        }

        collection.insert(drink_document)
        master_drink_list.append(drink_document)
        

    #pprint(drink_dict)
    with open('cocktaildb_drinks_data.pkl', 'w') as picklefile:
        pickle.dump(master_drink_list, picklefile)
