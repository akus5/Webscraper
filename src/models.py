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
    full_time = EmbeddedDocumentListField(EmbeddedDocumentField(Bet1X2))
    first_half = EmbeddedDocumentListField(EmbeddedDocumentField(Bet1X2))
    secound_half = EmbeddedDocumentListField(EmbeddedDocumentField(Bet1X2))


class BetAH(EmbeddedDocument):
    handicap = StringField(max_length=64, required=True)
    _1 = FloatField(required=True)
    _2 = FloatField(required=True)
    payout = FloatField(required=True)


class AsianHandicap(EmbeddedDocument):
    full_time = EmbeddedDocumentListField(EmbeddedDocumentField(BetAH))
    first_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetAH))
    secound_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetAH))


class BetOU(EmbeddedDocument):
    handicap = StringField(max_length=64, required=True)
    over = FloatField(required=True)
    under = FloatField(required=True)
    payout = FloatField(required=True)


class OverUnder(EmbeddedDocument):
    full_time = EmbeddedDocumentListField(EmbeddedDocumentField(BetOU))
    first_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetOU))
    secound_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetOU))


class BetDNB(EmbeddedDocument):
    bookmaker = StringField(max_length=64, required=True)
    _1 = FloatField(required=True)
    _2 = FloatField(required=True)
    payout = FloatField(required=True)


class DrawNoBet(EmbeddedDocument):
    full_time = EmbeddedDocumentListField(EmbeddedDocumentField(BetDNB))
    first_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetDNB))
    secound_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetDNB))


class BetEH(EmbeddedDocument):
    handicap = StringField(max_length=64, required=True)
    _1 = FloatField(required=True)
    _X = FloatField(required=True)
    _2 = FloatField(required=True)
    payout = FloatField(required=True)


class EuropeanHandicap(EmbeddedDocument):
    full_time = EmbeddedDocumentListField(EmbeddedDocumentField(BetEH))
    first_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetEH))
    secound_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetEH))


class BetDC(EmbeddedDocument):
    bookmaker = StringField(max_length=64, required=True)
    _1X = FloatField(required=True)
    _12 = FloatField(required=True)
    _X2 = FloatField(required=True)
    payout = FloatField(required=True)


class DoubleChance(EmbeddedDocument):
    full_time = EmbeddedDocumentListField(EmbeddedDocumentField(BetDC))
    first_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetDC))
    secound_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetDC))


class BetCS(EmbeddedDocument):
    score = StringField(max_length=5, required=True)
    odds = FloatField(required=True)


class CorrectScore(EmbeddedDocument):
    full_time = EmbeddedDocumentListField(EmbeddedDocumentField(BetCS))
    first_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetCS))
    secound_half = EmbeddedDocumentListField(EmbeddedDocumentField(BetCS))


class Bets(EmbeddedDocument):
    one_x_two = EmbeddedDocumentListField(EmbeddedDocumentField(OneXTwo))
    asian_handicap = EmbeddedDocumentListField(EmbeddedDocumentField(AsianHandicap))
    over_under = EmbeddedDocumentListField(EmbeddedDocumentField(OverUnder))
    draw_no_bet = EmbeddedDocumentListField(EmbeddedDocumentField(DrawNoBet))
    european_handicap = EmbeddedDocumentListField(EmbeddedDocumentField(EuropeanHandicap))
    double_chance = EmbeddedDocumentListField(EmbeddedDocumentField(DoubleChance))
    correct_score = EmbeddedDocumentListField(EmbeddedDocumentField(CorrectScore))
    bets_date = DateTimeField(default=datetime.datetime.now())


class Match(Document):
    title = StringField(max_length=258, required=True)
    team_home = StringField(max_length=128, required=True)
    team_away = StringField(max_length=128, required=True)
    league = StringField(max_length=128, required=False)
    country = StringField(max_length=128, required=True)
    match_date = DateTimeField(required=True)
    bets = EmbeddedDocumentListField(EmbeddedDocumentField(Bets))

    link = URLField()
    create_date = DateTimeField(default=datetime.datetime.now())
