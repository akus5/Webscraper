from bs4 import BeautifulSoup
import requests


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
print(get_href(soup))

for x in get_href(soup):
    print(request("http://www.oddsportal.com"+x))




