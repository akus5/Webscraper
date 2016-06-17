from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from contextlib import contextmanager
import time
import re
from webscraper.models import *
import datetime
from pytz import timezone as tz, utc


urls = []

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
        'minor_fields': ['bookmaker', '_1', '_2', 'payout'],
        'bets_field': 'draw_no_bet',
    },
    'DC': {
        'major_model': DoubleChance,
        'minor_model': BetDC,
        'minor_fields': ['bookmaker', '_1X', '_12', '_X2', 'payout'],
        'bets_field': 'double_chance',
    },
    'AH': {
        'major_model': AsianHandicap,
        'minor_model': BetAH,
        'minor_fields': ['handicap', '_1', '_2', 'payout'],
        'bets_field': 'asian_handicap',
    },
    'O/U': {
        'major_model': OverUnder,
        'minor_model': BetOU,
        'minor_fields': ['handicap', 'over', 'under', 'payout'],
        'bets_field': 'over_under',
    },
    'EH': {
        'major_model': EuropeanHandicap,
        'minor_model': BetEH,
        'minor_fields': ['handicap', '_1', '_X', '_2', 'payout'],
        'bets_field': 'european_handicap',
    },
}


class MatchPageScraper:

    def __init__(self, url):
        self.driver = webdriver.Opera()
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
            skipped = False
            link['bet_type'].click()
            time.sleep(1)
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
                time.sleep(1)
                if link['bet_name'] == 'AH':
                    data = self.get_asian_handicap_bets_data()
                elif link['bet_name'] == 'O/U':
                    data = self.get_over_under_bets_data()
                elif link['bet_name'] == 'EH':
                    data = self.get_european_handicap_bets_data()
                else:
                    data = self.get_bets_data()
                    pass
                data[:] = [item for item in data if len(item) == len(bet_config['minor_fields'])]
                time_type = bet.text
                print('typ={}, czas={}, bety={}'.format(link['bet_name'], time_type, data))
                try:
                    if '/' in data[0][1] or '+' in data[0][1] or '-' in data[0][1]:
                        print('skipped')
                        skipped = True
                        break
                except IndexError:
                    pass
                for i in range(len(data)):
                    minor_obj = bet_config['minor_model']()
                    for j, field in enumerate(bet_config['minor_fields']):
                        if field not in ['bookmaker', 'handicap']:
                            setattr(minor_obj, field, float(data[i][j]))
                        else:
                            setattr(minor_obj, field, data[i][j])
                    getattr(major_obj, time_types[time_type]).append(minor_obj)
            if not skipped:
                setattr(bets_obj, bet_config['bets_field'], major_obj)
        return bets_obj

    def get_asian_handicap_bets_data(self):
        page_source = self.get_source_code()
        data = []
        odds_data_table = page_source.find('div', {'id': 'odds-data-table'})
        table_header_light = odds_data_table.select('div[class^=table-header-light]')
        for tag in table_header_light:
            text = tag.text.split('(')
            if text[1].startswith('0'):
                continue
            data_text = text[0].split()
            handicap = ' '.join(data_text[:3])
            bet_values = data_text[3].split('%')
            payout = bet_values[0]
            values = bet_values[1].split('.')
            _1 = ''.join((values[0], '.', values[1][:2]))
            _2 = ''.join((values[1][2:], '.', values[2]))
            data.append([handicap, _1, _2, payout])
        return data

    def get_european_handicap_bets_data(self):
        page_source = self.get_source_code()
        data = []
        odds_data_table = page_source.find('div', {'id': 'odds-data-table'})
        table_header_light = odds_data_table.select('div[class^=table-header-light]')
        for tag in table_header_light:
            text = tag.text.split('(')
            if text[1].startswith('0'):
                continue
            data_text = text[0].split()
            handicap = ' '.join(data_text[:3])
            bet_values = data_text[3].split('%')
            payout = bet_values[0]
            values = bet_values[1].split('.')
            _1 = ''.join((values[0], '.', values[1][:2]))
            _X = ''.join((values[1][2:], '.', values[2][:2]))
            _2 = ''.join((values[2][2:], '.', values[3]))
            data.append([handicap, _1, _X, _2, payout])
        return data

    def get_over_under_bets_data(self):
        page_source = self.get_source_code()
        data = []
        odds_data_table = page_source.find('div', {'id': 'odds-data-table'})
        table_header_light = odds_data_table.select('div[class^=table-header-light]')
        for tag in table_header_light:
            text = tag.text.split('(')
            if text[1].startswith('0'):
                continue
            data_text = text[0].split()
            handicap = ' '.join(data_text[:2])
            bet_values = data_text[2].split('%')
            payout = bet_values[0]
            values = bet_values[1].split('.')
            over = ''.join((values[0], '.', values[1][:2]))
            under = ''.join((values[1][2:], '.', values[2]))
            data.append([handicap, over, under, payout])
        return data

    def get_bets_data(self):
        page_source = self.get_source_code()
        data = []
        for bet in page_source.tbody:
            try:
                name, value = bet.get_text().rsplit(None, 1)
            except:
                break
            data.append([name[1:]] + re.findall('....', value))
        return data

    def get_match_info(self):
        page_source = self.get_source_code()
        page_title = page_source.title.string.replace('Betting Odds', '')
        splited_page_title = page_title.split(',')
        title = splited_page_title[0].rstrip()
        team_home = title.split('-')[0].rstrip()
        team_away = title.split('-')[1].rstrip().lstrip()
        league = splited_page_title[1].split('-')[1].lstrip()
        match_date_str = page_source.select("p[class^=date]")[0].string.replace(',', '').replace('  ', ' ')
        match_date = datetime.datetime.strptime(match_date_str, '%A %d %b %Y %H:%M')
        end_date = match_date + datetime.timedelta(minutes=110)
        info = {
            'title': title,
            'team_home': team_home,
            'team_away': team_away,
            'league': league,
            'match_date': match_date,
            'end_date': end_date,
            'link': self.driver.current_url,
        }
        return info

    def get_score(self):
        page_source = self.get_source_code()
        score = page_source.select_one('.result')
        score_text = score.text.replace('Final result ', '')
        return score_text


class NewMatchScraper:

    def __init__(self):
        self.driver = webdriver.Opera()
        self.base_url = 'http://www.oddsportal.com/matches/soccer/'
        self.url = self.get_page_url()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get_source_code(self):
        self.driver.get(self.url)
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def get_page_url(self):
        date = str(datetime.datetime.now(utc) + datetime.timedelta(days=6))
        date = date.split()[0].replace('-', '')
        return self.base_url + date

    def get_links(self):
        page_source = self.get_source_code()
        links = []
        main_table = page_source.find('table', {'class': ' table-main'})
        tbody = main_table.find('tbody')
        black_list = tbody.select('.dark')
        trs = [tr for tr in tbody.find_all('tr') if tr not in black_list]
        for tr in trs:
            all_a = tr.find_all('a')
            for a in all_a:
                if str(a.get('href')).startswith('/soccer/'):
                    links.append('http://www.oddsportal.com' + a.get('href'))
        return links

