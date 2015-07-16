#!/usr/bin/env python
import sys
import requests
import re
import pickle

from bs4 import BeautifulSoup
from pprint import pprint


base_url = "http://wiki.webtender.com"
drink_dict = {}

def get_soup(extended_url="", level="all"):
    url = base_url + extended_url
    response = requests.get(url)
    page = response.text
    if level == "all":
        soup_id = "mw-pages"
    elif level == "drink":
        soup_id="bodyContent"
    soup = BeautifulSoup(page, "lxml").find(id = soup_id)
    return soup

def has_next_page(soup):
    next_page_url = soup.find_all("a")[-1]["href"]
    if "pagefrom" in next_page_url:
    # else this function returns None.
        return next_page_url

def get_drink_links_from_soup(soup):
    drink_list_elements = soup.find_all("li")
    for li in drink_list_elements:
        link = li.find("a")
        drink_dict[link["title"]] = {"link": link["href"]}
    
def drink_links(url="/wiki/Category:Recipes"):
    soup = get_soup(extended_url=url)
    get_drink_links_from_soup(soup)
    next_page = has_next_page(soup)
    next_page = False
    if next_page:
        drink_links(url=next_page)

def get_drink_info(soup, drink_name):
    # get ingredients    
    ingredients = []
    print >> sys.stderr, "getting %s" % drink_name
    recipe_regex = re.compile('recipe', re.IGNORECASE)
    try:
        # try to properly look for 
        for element in soup.find(id=recipe_regex).find_next("ul").find_all('li'):
            ingredients.append(element.text.strip())
            drink_dict[drink_name]["ingredients"] = ingredients
    except AttributeError:
        print >> sys.stderr, "looking the brutish way for %s" % drink_name
        for element in soup.find("ul").find_all("li"):
            ingredients.append(element.text.strip())
            drink_dict[drink_name]["ingredients"] = ingredients

    # get instructions
    all_text = soup.find_all("p")
    if all_text:
        instructions = all_text.pop().text.strip()
    else:
        instructions = ""
    ## alternatively:
    #soup.find("ul").next_sibling.next_sibling
    drink_dict[drink_name]["instructions"] = instructions

    # get background drink info
    background = "\n".join([remaining_text.text.strip() 
                            for remaining_text in all_text])
    drink_dict[drink_name]["background"] = background



if __name__ == '__main__':
    drink_links()
    for drink_name, drink_level_dict in drink_dict.iteritems():
        drink_level_soup = get_soup(extended_url = drink_level_dict["link"], 
                                    level = "drink",
                                )
        get_drink_info(drink_level_soup, drink_name)
    with open('drinks_data.pkl', 'w') as picklefile:
        pickle.dump(drink_dict, picklefile)
    
    

    


