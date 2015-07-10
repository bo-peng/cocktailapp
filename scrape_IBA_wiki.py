#!/usr/bin/env python
import sys
import requests
import re

from bs4 import BeautifulSoup
from pymongo import MongoClient
from pprint import pprint

from scrape_cocktaildb import open_mongo_connection


def get_soup():
    url = "https://en.wikipedia.org/wiki/List_of_IBA_official_cocktails"
    response = requests.get(url)
    page = response.text
    return BeautifulSoup(page, "lxml")


if __name__ == '__main__':
    types = ["The Unforgettables", "Contemporary Classics", "New Era Drinks"]
    soup = get_soup()

    collection = open_mongo_connection()

    for drink_type, drink_list in zip(types, soup.find_all("table", {"class": "multicol"})):
        print
        print drink_type
        for i, a_link in enumerate(drink_list.find_all("a", {"title": True})):
            drink_name =  a_link.text
            #collection.update({"name": drink_name},
            #                  {"$set": {"recognitions": {"IBA": drink_type}}})
            print i, drink_name
            if not collection.find({"name": drink_name}):
                print drink_name
                import pdb; pdb.set_trace()


