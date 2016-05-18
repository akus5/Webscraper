from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from random import randint
import re
import itertools

urls = []
bet_1x2 = {'full_time': '#1X2;2', 'first_half': '#1X2;3', 'second_half': '#1X2;4'}
bet_dnb = {'full_time': '#dnb;2', 'first_half': '#dnb;3', 'second_half': '#dnb;4'}
bet_double = {'full_time': '#double;2', 'first_half': '#double;3', 'second_half': '#double;4'}
bet_toqualify = {'FT_including_OT': '#qualify;1'}
bet_oddoreven = {'full_time': '#odd-even;2', 'first_half': '#odd-even;3', 'second_half': '#odd-even;4'}
bet_bts = {'full_time': '#bts;2', 'first_half': '#bts;3', 'second_half': '#bts;4'}
bets = {'1X2': bet_1x2, 'DNB': bet_dnb, 'DC': bet_double, 'TQ': bet_toqualify, 'Odd-Even': bet_oddoreven, 'BTS': bet_bts}


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
        self.driver.find_element_by_tag_name('body').send_keys("\uE035")
        self.driver.get(url)
        return self.driver.page_source


class GetData:

    def get_href(self, page_source):
        list1 = []
        for url in page_source.find_all("table", {"id": "sport_content_soccer_all"})[0].find_all("a", {"foo": "f"}):
            if str(url.get('href')).startswith('/soccer/'):
                list1.append('http://www.oddsportal.com' + url.get('href'))
        return list1

    def get_href2(self, page_source):
        list2 = []
        for url in page_source.tbody.find_all("a"):
            if str(url.get('href')).startswith('/soccer/'):
                list2.append('http://www.oddsportal.com' + url.get('href'))
        return list2[3:]

    def get_data1x2(self, page_source):
        lst1 = {}
        for bet in page_source.tbody:
            try:
                name, value = bet.get_text().rsplit(None, 1)
            except:
                break
            lst1[name[1:]] = re.findall('....', value)
        return page_source.h1.string, page_source.select("p[class^=date]")[0].string, lst1

    def get_data(self, link):
        for key, bet in bets.items():
            for key1, rest in bet.items():
                with WebScraper() as scraper1:
                    print(key + " " + key1)
                    print(self.get_data1x2(scraper1.get_source_code(link + rest)))





get = GetData()

with WebScraper() as scraper:
    links = get.get_href(scraper.get_source_code('http://www.oddsportal.com/events/'))
    print(links)
    for x in links:
        try:
            ln = get.get_href2(scraper.get_source_code(x))
            # urls.append(ln)
            print("Pobrano linki z :" + x)
        except:
            time.sleep(randint(0, 9))
        for link in ln:
            try:
                print(get.get_data(link))
            except:
                time.sleep(randint(0, 9))

'''
for link in list(itertools.chain.from_iterable(urls)):
    try:
        print(get_data1x2(scraper.get_source_code(link)))
    except:
        time.sleep(randint(0, 9))
'''



'''
def request(link):
    r = requests.get(link)
    data = r.text
    return BeautifulSoup(data, 'html.parser')


'''



