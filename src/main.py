from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from random import randint


class WebScraper:

    def __init__(self):
        self.driver = webdriver.Firefox()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get_source_code(self, url):
        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def get_plain_source_code(self, url):
        self.driver.get(url)
        return self.driver.page_source


def get_href(page_source):
    list1 = []
    for link in page_source.find_all("a", {"foo": "f"}):
        if str(link.get('href')).startswith('/soccer/'):
            list1.append('http://www.oddsportal.com' + link.get('href'))
    return list1


def get_href2(page_source):
    list2 = []
    print(page_source.tbody)
    for link in page_source.tbody.find_all("a"):
        if str(link.get('href')).startswith('/soccer/'):
            list2.append('http://www.oddsportal.com' + link.get('href'))
    return list2[3:]

with WebScraper() as scraper:
    links = get_href(scraper.get_source_code('http://www.oddsportal.com/events/'))
    print(links)
    for x in links:
        try:
            print(get_href2(scraper.get_source_code(x)))
        except:
            time.sleep(randint(0, 9))


'''
def request(link):
    r = requests.get(link)
    data = r.text
    return BeautifulSoup(data, 'html.parser')


'''



