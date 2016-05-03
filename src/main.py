from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from random import randint

urls = []


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
    for url in page_source.find_all("a", {"foo": "f"}):
        if str(url.get('href')).startswith('/soccer/'):
            list1.append('http://www.oddsportal.com' + url.get('href'))
    return list1


def get_href2(page_source):
    list2 = []
    for url in page_source.tbody.find_all("a"):
        if str(url.get('href')).startswith('/soccer/'):
            list2.append('http://www.oddsportal.com' + url.get('href'))
    return list2[3:]


def get_data(page_source):
    return page_source.h1.string, page_source.select("p[class^=date]")


with WebScraper() as scraper:
    links = get_href(scraper.get_source_code('http://www.oddsportal.com/events/'))
    for x in links:
        try:
            urls.append(get_href2(scraper.get_source_code(x)))
        except:
            time.sleep(randint(0, 9))
    for link in urls:
        print(get_data(scraper.get_source_code(link)))



'''
def request(link):
    r = requests.get(link)
    data = r.text
    return BeautifulSoup(data, 'html.parser')


'''



