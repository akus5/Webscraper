import datetime

from mongoengine import *


connect('scrapper', host='mongodb://localhost/scrapper')


class Match(Document):
    team_home = StringField(max_length=128, required=True)
    team_away = StringField(max_length=128, required=True)
    date = DateTimeField()

"""
class Match(Document):
    title = StringField(max_length=200, required=True)
    created_at = DateTimeField(default=datetime.datetime.now)

test_match = Match(title='Lech Poznań vs Legia Warszawa')
test_match.save()

"""

