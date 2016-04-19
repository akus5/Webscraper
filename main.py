from bs4 import BeautifulSoup

import requests

r = requests.get("http://www.oddsportal.com/")

data = r.text

soup = BeautifulSoup(data)

for link in soup.find_all('a'):
    print(link.get('href'))
