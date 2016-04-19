import datetime

from mongoengine import *


connect('scrapper', host='mongodb://localhost/scrapper')


class Match(Document):
    title = StringField(max_length=200, required=True)
    created_at = DateTimeField(default=datetime.datetime.now)

test_match = Match(title='Lech Poznań vs Legia Warszawa')
test_match.save()



