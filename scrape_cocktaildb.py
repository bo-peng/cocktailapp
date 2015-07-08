#!/usr/bin/env python
import sys
import requests
import re
import pickle

from bs4 import BeautifulSoup
from pprint import pprint


def get_soup(drink_id_number, base_url = "http://cocktaildb.com"):
    url = base_url + "/recipe_detail?id=" + str(drink_id_number)
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    return soup



def get_ingredients(soup, ingredients=[]):
    for recipeMeasure in soup.find_all("div", {"class": "recipeMeasure"}):
        ingredient = " or ".join([a.text for a in recipeMeasure.find_all("a")])
        measure = recipeMeasure.text.split(ingredient)[0].strip()
        ingredients.append([ingredient, measure])

        # alternate measure units
        # recipeMeasure.find("span", {"class": "recipeAltUnits"}).text 
        #print "INGREDIENT", ingredient, "MEASURE", measure
    return ingredients

def get_instructions_and_glass(soup, instructions=[], glass_type=None):
    for recipeDirection in soup.find_all("div", {"class": "recipeDirection"}):
        instruction_text = recipeDirection.text
        if "glass" in instruction_text and bool(recipeDirection.find("a")):
            glass_type = recipeDirection.find("a").text
        instructions.append(instruction_text)
    return instructions, glass_type
    
if __name__ == '__main__':
    #recipes go from 1 to 4758
    #for i in range(1, 4758+1):
    drink_dict = {}
    for i in range(5, 15):
        soup = get_soup(i)
        
        # get drink name
        drink_name = soup.find(id="wellTitle").find("h2").text
        
        ingredients = get_ingredients(soup)
        instructions, glass_type = get_instructions_and_glass(soup)
        
        drink_dict[drink_name] = {"ingredients": ingredients,
                                  "instructions": instructions,
                                  "glass_type": glass_type,
                                  "site_id": i,
                              }

    pprint(drink_dict)
