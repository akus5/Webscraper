from bs4 import BeautifulSoup
import requests
from selenium import webdriver


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


with WebScraper() as scraper:
    print(len(scraper.get_source_code('http://www.oddsportal.com/matches/soccer/20160420/').text))
    print(len(scraper.get_source_code('http://www.oddsportal.com/matches/soccer/20160421/').text))

'''
def request(link):
    r = requests.get(link)
    data = r.text
    return BeautifulSoup(data, 'html.parser')


def get_href(soup):
    list = []
    for link in soup.find_all('a'):
        if str(link.get('href')).startswith('/soccer/'):   #dałam tylko dla pilki noznej na razie
            list.append(link.get('href'))
    return list

soup = request("http://www.oddsportal.com/events/")
# print(get_href(soup))

# for x in get_href(soup):
    # print(request("http://www.oddsportal.com"+x))
'''



