import datetime

from mongoengine import *


connect('scrapper', host='mongodb://localhost/scrapper')


class Bet1X2(EmbeddedDocument):
    bookmaker = StringField(max_length=64, required=True)
    _1 = FloatField(required=True)
    _X = FloatField(required=True)
    _2 = FloatField(required=True)
    payout = FloatField(required=True)


class OneXTwo(EmbeddedDocument):
    full_time = ListField(EmbeddedDocumentField(Bet1X2))
    first_half = ListField(EmbeddedDocumentField(Bet1X2))
    secound_half = ListField(EmbeddedDocumentField(Bet1X2))


class BetAH(EmbeddedDocument):
    handicap = StringField(max_length=64, required=True)
    _1 = FloatField(required=True)
    _2 = FloatField(required=True)
    payout = FloatField(required=True)


class AsianHandicap(EmbeddedDocument):
    full_time = ListField(EmbeddedDocumentField(BetAH))
    first_half = ListField(EmbeddedDocumentField(BetAH))
    secound_half = ListField(EmbeddedDocumentField(BetAH))


class BetOU(EmbeddedDocument):
    handicap = StringField(max_length=64, required=True)
    over = FloatField(required=True)
    under = FloatField(required=True)
    payout = FloatField(required=True)


class OverUnder(EmbeddedDocument):
    full_time = ListField(EmbeddedDocumentField(BetOU))
    first_half = ListField(EmbeddedDocumentField(BetOU))
    secound_half = ListField(EmbeddedDocumentField(BetOU))


class BetDNB(EmbeddedDocument):
    bookmaker = StringField(max_length=64, required=True)
    _1 = FloatField(required=True)
    _2 = FloatField(required=True)
    payout = FloatField(required=True)


class DrawNoBet(EmbeddedDocument):
    full_time = ListField(EmbeddedDocumentField(BetDNB))
    first_half = ListField(EmbeddedDocumentField(BetDNB))
    secound_half = ListField(EmbeddedDocumentField(BetDNB))


class BetEH(EmbeddedDocument):
    handicap = StringField(max_length=64, required=True)
    _1 = FloatField(required=True)
    _X = FloatField(required=True)
    _2 = FloatField(required=True)
    payout = FloatField(required=True)


class EuropeanHandicap(EmbeddedDocument):
    full_time = ListField(EmbeddedDocumentField(BetEH))
    first_half = ListField(EmbeddedDocumentField(BetEH))
    secound_half = ListField(EmbeddedDocumentField(BetEH))


class BetDC(EmbeddedDocument):
    bookmaker = StringField(max_length=64, required=True)
    _1X = FloatField(required=True)
    _12 = FloatField(required=True)
    _X2 = FloatField(required=True)
    payout = FloatField(required=True)


class DoubleChance(EmbeddedDocument):
    full_time = ListField(EmbeddedDocumentField(BetDC))
    first_half = ListField(EmbeddedDocumentField(BetDC))
    secound_half = ListField(EmbeddedDocumentField(BetDC))


class BetCS(EmbeddedDocument):
    score = StringField(max_length=5, required=True)
    odds = FloatField(required=True)


class CorrectScore(EmbeddedDocument):
    full_time = ListField(EmbeddedDocumentField(BetCS))
    first_half = ListField(EmbeddedDocumentField(BetCS))
    secound_half = ListField(EmbeddedDocumentField(BetCS))


class Bets(EmbeddedDocument):
    one_x_two = ListField(EmbeddedDocumentField(OneXTwo))
    asian_handicap = ListField(EmbeddedDocumentField(AsianHandicap))
    over_under = ListField(EmbeddedDocumentField(OverUnder))
    draw_no_bet = ListField(EmbeddedDocumentField(DrawNoBet))
    european_handicap = ListField(EmbeddedDocumentField(EuropeanHandicap))
    double_chance = ListField(EmbeddedDocumentField(DoubleChance))
    correct_score = ListField(EmbeddedDocumentField(CorrectScore))
    bets_date = DateTimeField(default=datetime.datetime.now())


class BaseMatch(Document):
    title = StringField(max_length=258, required=True)
    team_home = StringField(max_length=128, required=True)
    team_away = StringField(max_length=128, required=True)
    league = StringField(max_length=128, required=False)
    country = StringField(max_length=128, required=True)
    match_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    bets = EmbeddedDocumentListField(Bets)

    link = URLField()
    create_date = DateTimeField(default=datetime.datetime.now())

    meta = {
        'abstract': True,
    }


class FinishedMatch(BaseMatch):
    score = StringField(max_length=5, required=True)

    def create_from_match(self, match, score):
        self.title = match.title
        self.team_away = match.team_away
        self.team_home = match.team_home
        self.league = match.league
        self.country = match.country
        self.match_date = match.match_date
        self.bets = match.bets
        self.link = match.link
        self.score = score
        return self

    meta = {'collection': 'finished_match'}


class Match(BaseMatch):
    meta = {'collection': 'match'}


# o = FinishedMatch.objects.get(country='Poland', team_home='Test')
# print(o.title)
# obj = Match(match_date=datetime.datetime.now() + datetime.timedelta(hours=4), team_home='Test', title='Druzyna3 vs Druzyna4', country='Poland', team_away='Druzyna4')
# b = Bet1X2(bookmaker='Test', _1=2.5, _X=2.5, _2=2.6, payout=96.56)
# o = OneXTwo()
# o.full_time.append(b)
# bet = Bets()
# bet.one_x_two.append(o)
#
# obj.bets.append(bet)
# obj.save()
# t = FinishedMatch().create_from_match(obj, '2:5')
# t.save()
