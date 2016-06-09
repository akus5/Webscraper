from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from contextlib import contextmanager
import time
from random import randint
import re
import itertools
from webscraper.models import *

urls = []
# bet_1x2 = {'full_time': '#1X2;2', 'first_half': '#1X2;3', 'second_half': '#1X2;4'}
# bet_dnb = {'full_time': '#dnb;2', 'first_half': '#dnb;3', 'second_half': '#dnb;4'}
# bet_double = {'full_time': '#double;2', 'first_half': '#double;3', 'second_half': '#double;4'}
# bet_toqualify = {'FT_including_OT': '#qualify;1'}
# bet_oddoreven = {'full_time': '#odd-even;2', 'first_half': '#odd-even;3', 'second_half': '#odd-even;4'}
# bet_bts = {'full_time': '#bts;2', 'first_half': '#bts;3', 'second_half': '#bts;4'}
# bets = {'1X2': bet_1x2, 'DNB': bet_dnb, 'DC': bet_double, 'TQ': bet_toqualify, 'Odd-Even': bet_oddoreven, 'BTS': bet_bts}

time_types = {
    'Full Time': 'full_time',
    '1st Half': 'first_half',
    '2nd Half': 'secound_half',
}


bets = {
    '1X2': {
        'major_model': OneXTwo,
        'minor_model': Bet1X2,
        'minor_fields': ['bookmaker', '_1', '_X', '_2', 'payout'],
        'bets_field': 'one_x_two',
    },
    'DNB': {
        'major_model': DrawNoBet,
        'minor_model': BetDNB,
        'bets_field': 'draw_no_bet',
    },
    'DC': {
        'major_model': DoubleChance,
        'minor_model': BetDC,
        'bets_field': 'double_chance',
    }
}


class MatchPage:

    def __init__(self, url):
        # self.driver = webdriver.PhantomJS(executable_path=r'C:\Users\Dawid\AppData\Roaming\npm\node_modules\phantomjs\lib\phantom\bin\phantomjs.exe')
        self.driver = webdriver.Firefox()
        self.url = url
        self.driver.get(url)
        self.bets = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get_source_code(self):
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.driver.find_element_by_id('odds-data-table')
        yield
        WebDriverWait(self.driver, timeout).until(
            staleness_of(old_page)
        )

    def get_types_links(self):
        bet_type_links = []
        tab = self.driver.find_element_by_id('tab-nav-main')
        ul = tab.find_element_by_class_name('ul-nav')
        lis = ul.find_elements_by_tag_name('li')
        for li in lis:
            if li.text in bets.keys():
                bet_type_links.append(
                    {
                        'bet_name': li.text,
                        'bet_type': li,
                        'time_types': []
                    })
        return bet_type_links

    def get_bets(self):
        bets_obj = Bets()
        links = self.get_types_links()
        for link in links:
            link['bet_type'].click()
            time.sleep(1.12)
            time_type = self.driver.find_element_by_id('bettype-tabs-scope')
            time_type_uls = time_type.find_elements_by_tag_name('ul')
            for ul in time_type_uls:
                if ul.get_attribute('style') == 'display: block;':
                    lis = ul.find_elements_by_tag_name('li')
                    link['time_types'].extend(lis)
            bet_config = bets[link['bet_name']]
            major_obj = bet_config['major_model']()
            for bet in link['time_types']:
                bet.click()
                time.sleep(1.2)
                data = self.get_bets_data(self.get_source_code())
                data = [item for item in data if len(item) == 5]
                time_type = bet.text
                print('typ={}, czas={}, bety={}'.format(link['bet_name'], time_type, data))
                for i in range(len(data)):
                    minor_obj = bet_config['minor_model']()
                    for j, field in enumerate(bet_config['minor_fields']):
                        setattr(minor_obj, field, data[i][j])
                    # setattr(major_obj, time_types[time_type], minor_obj)
                    getattr(major_obj, time_types[time_type]).append(minor_obj)
            major_obj
            pass


                # setattr(bets, bet_config['bets_field'], )

        # print(links)

    def get_bets_data(self, page_source):
        lst1 = []
        for bet in page_source.tbody:
            try:
                name, value = bet.get_text().rsplit(None, 1)
            except:
                break
            lst1.append([name[1:]] + re.findall('....', value))
        return lst1  # page_source.select("p[class^=date]")[0].string, page_source.h1.string

        # #print(links)
        # #a = li.find_element_by_tag_name('a')
        # print(links[1].get_attribute('innerHTML'))
        # a = links[1].find_element_by_tag_name('a')
        # # print('len before {}'.format(len(self.driver.page_source)))
        # print(a.get_attribute('innerHTML'))
        #
        # # actions = ActionChains(self.driver)
        # # actions.click(links[1])
        # # actions.perform()
        # # a.click()
        # links[1].click()
        # time.sleep(0.5)
        # # with self.wait_for_page_load(timeout=20):
        # time_types = self.driver.find_element_by_id('odds-data-table')  # .get_attribute('innerHTML')
        # rr = self.driver.find_element_by_class_name('table-container') #.get_attribute('innerHTML')
        # rr_html = rr.get_attribute('innerHTML')
        # # print('len after {}'.format(len(self.driver.page_source)))
        # gg = rr.find_element_by_tag_name('tbody')
        # print(gg.get_attribute('innerHTML'))
        # # ul = time_types.find_element_by_tag_name('ul')
        # # li_s = ul.find_elements_by_tag_name('li')
        # # tabs = time_types.find_elements_by_tag_name('li')
        # # tabs[1].click()
        # # # table = self.driver.find_element_by_id('odds-data-table')
        # # table = self.driver.find_elements_by_class_name('detail-odds')
        # # table_html = table[0].get_attribute('innerHTML')
        # # print(table_html)
        # pass


class WebScraper:

    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path=r'C:\Users\Dawid\AppData\Roaming\npm\node_modules\phantomjs\lib\phantom\bin\phantomjs.exe')
        self.base_url = 'http://www.oddsportal.com'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get_source_code(self, url):
        self.driver.get(url)
        # WebDriverWait(self.driver, timeout=500)
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def get_plain_source_code(self, url):
        self.driver.get(url)
        self.driver.find_element_by_tag_name('body').send_keys("\uE035")
        self.driver.get(url)
        return self.driver.page_source

    def get_href(self, page_source):
        list1 = []
        for url in page_source.find_all("table", {"id": "sport_content_soccer_all"})[0].find_all("a", {"foo": "f"}):
            if str(url.get('href')).startswith('/soccer/'):
                list1.append('http://www.oddsportal.com' + url.get('href'))
        return list1

    def get_data1x2(self, page_source):
        lst1 = {}
        for bet in page_source.tbody:
            try:
                name, value = bet.get_text().rsplit(None, 1)
            except:
                break
            lst1[name[1:]] = re.findall('....', value)
        return page_source.h1.string, page_source.select("p[class^=date]")[0].string, lst1

    def get_href2(self, page_source):
        list2 = []
        for url in page_source.tbody.find_all("a"):
            if str(url.get('href')).startswith('/soccer/'):
                list2.append('http://www.oddsportal.com' + url.get('href'))
        return list2[3:]

    def get_types_links(self, url):
        self.driver.get(url)
        tab = self.driver.find_element_by_id('tab-nav-main')
        print(tab.find_element_by_class_name('ul-nav'))

    def get_match_bets(self, url):
        for key, bet in bets.items():
            for key1, rest in bet.items():
                # print(self.get_data1x2(self.get_source_code(url + rest)))
                print('{}'.format(key1))
                self.get_types_links(url+rest)

#
# # with WebScraper() as scraper:
#     # scraper.get_match_bets('http://www.oddsportal.com/soccer/europe/baltic-cup-u21/latvia-lithuania-A3ePitV9/')
#
with MatchPage('http://www.oddsportal.com/soccer/brazil/serie-b/luverdense-atletico-go-xYF3gSuA/') as page:
    page.get_bets()

#
# class WebScraper:
#
#     def __init__(self):
#         self.driver = webdriver.PhantomJS(executable_path=r'C:\Users\Dawid\AppData\Roaming\npm\node_modules\phantomjs\lib\phantom\bin\phantomjs.exe')
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.driver.close()
#
#     def get_source_code(self, url):
#         self.driver.get(url)
#         return BeautifulSoup(self.driver.page_source, 'html.parser')
#
#     def get_plain_source_code(self, url):
#         self.driver.get(url)
#         self.driver.find_element_by_tag_name('body').send_keys("\uE035")
#         self.driver.get(url)
#         return self.driver.page_source
#
#
#
# class GetData:
#
#     def get_href(self, page_source):
#         list1 = []
#         for url in page_source.find_all("table", {"id": "sport_content_soccer_all"})[0].find_all("a", {"foo": "f"}):
#             if str(url.get('href')).startswith('/soccer/'):
#                 list1.append('http://www.oddsportal.com' + url.get('href'))
#         return list1
#
#     def get_href2(self, page_source):
#         list2 = []
#         for url in page_source.tbody.find_all("a"):
#             if str(url.get('href')).startswith('/soccer/'):
#                 list2.append('http://www.oddsportal.com' + url.get('href'))
#         return list2[3:]
#
#     def get_data1x2(self, page_source):
#         lst1 = {}
#         for bet in page_source.tbody:
#             try:
#                 name, value = bet.get_text().rsplit(None, 1)
#             except:
#                 break
#             lst1[name[1:]] = re.findall('....', value)
#         return page_source.h1.string, page_source.select("p[class^=date]")[0].string, lst1
#
#     def get_data(self, link):
#         for key, bet in bets.items():
#             for key1, rest in bet.items():
#                 with WebScraper() as scraper1:
#                     print(key + " " + key1)
#                     print(self.get_data1x2(scraper1.get_source_code(link + rest)))
#
# get = GetData()
#
# with WebScraper() as scraper:
#     links = get.get_href(scraper.get_source_code('http://www.oddsportal.com/events/'))
#     print(links)
#     for x in links:
#         try:
#             ln = get.get_href2(scraper.get_source_code(x))
#             # urls.append(ln)
#             print("Pobrano linki z :" + x)
#         except:
#             time.sleep(randint(0, 9))
#         for link in ln:
#             try:
#                 print(get.get_data(link))
#             except:
#                 time.sleep(randint(0, 9))

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



