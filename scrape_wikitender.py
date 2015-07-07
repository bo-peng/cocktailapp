import requests
from bs4 import BeautifulSoup
from pprint import pprint

base_url = "http://wiki.webtender.com"
drink_dict = {}

def get_soup(extended_url=""):
    url = base_url + extended_url
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml").find(id="mw-pages")
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
        drink_dict[link["title"]] = link["href"]
    
def drink_links(url="/wiki/Category:Recipes"):
    soup = get_soup(extended_url=url)
    get_drink_links_from_soup(soup)
    next_page = has_next_page(soup)
    if next_page:
        drink_links(url=next_page)

if __name__ == '__main__':
    drink_links()
    pprint(drink_dict)
    print len(drink_dict)
    


