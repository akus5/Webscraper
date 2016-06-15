from multiprocessing import Process
from time import sleep
from datetime import datetime as dt, timedelta
from pytz import timezone as tz
from threading import Thread


from webscraper.models import Match, FinishedMatch, WorkerInfo
from webscraper.scrapers import NewMatchScraper, MatchPageScraper


class Worker(Process):

    def __init__(self, worker_delay, model, data_delay=10, name='Worker'):
        super(Worker, self).__init__()
        self.worker_delay = worker_delay
        self.data_delay = data_delay
        self.name = name
        self.model = model
        self.data_provider = None

    def run(self):
        pass


class DataProvider(Thread):
    data = []

    def __init__(self, delay, model, name):
        super().__init__()
        self.delay = delay
        self.model = model
        self.data = []
        self.name = name
        self.setName('{}\'s data provider'.format(self.name))

    def update(self):
        pass

    def run(self):
        from os import getpid
        print('Running thread "{}" on process {}'.format(self.getName(), getpid()))
        while True:
            self.update()
            sleep(self.delay)


class TodayWorker(Worker):

    class TodayDataProvider(DataProvider):

        def update(self):
            self.data = self.model.objects(match_date__gte=dt.now(tz('UTC')), match_date__lte=dt.now(tz('UTC')) + timedelta(days=1))
            print('Znaleziono {} dzisiajszych meczy'.format(len(self.data)))

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = self.TodayDataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            # print(self.name)
            for match in self.data_provider.data:
                bets = None
                with MatchPageScraper(match.link) as scraper:
                    bets = scraper.get_bets()
                match.bets.append(bets)
                match.save()
                print('Zaktualizowano dzisiejszy mecz {}'.format(match.title))
            sleep(self.worker_delay)


class CurrentWorker(Worker):

    class CurrentDataProvider(DataProvider):

        def update(self):
            self.data = self.model.objects(end_date__gte=dt.now(tz('UTC')), end_date__lte=dt.now(tz('UTC')) + timedelta(minutes=110))
            print('Znaleziono {} trwających meczy'.format(len(self.data)))

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = self.CurrentDataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            # print(self.name)
            for match in self.data_provider.data:
                bets = None
                with MatchPageScraper(match.link) as scraper:
                    bets = scraper.get_bets()
                match.bets.append(bets)
                match.save()
                print('Zaktualizowano trwający mecz {}'.format(match.title))
            sleep(self.worker_delay)


class WeekWorker(Worker):

    class WeekDataProvider(DataProvider):

        def update(self):
            self.data = self.model.objects(match_date__gte=dt.now(tz('UTC')) + timedelta(days=1))
            print('Znaleziono {} meczy w tym tygodniu'.format(len(self.data)))

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = self.WeekDataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            # print(self.name)
            for match in self.data_provider.data:
                bets = None
                with MatchPageScraper(match.link) as scraper:
                    bets = scraper.get_bets()
                match.bets.append(bets)
                match.save()
                print('Zaktualizowano mecz {}'.format(match.title))
            sleep(self.worker_delay)


class EndedWorker(Worker):

    class EndedDataProvider(DataProvider):

        def update(self):
            self.data = self.model.objects(match_date__lte=(dt.now(tz('UTC')) - timedelta(minutes=115)))
            print('Znaleziono {} zakończonych meczy'.format(len(self.data)))

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = self.EndedDataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            # print(self.name)
            for match in self.data_provider.data:
                score = None
                with MatchPageScraper(match.link) as scraper:
                    score = scraper.get_score()
                finished = FinishedMatch().create_from_match(match, score)
                finished.save()
                print('Przeniesiono mecz {} do zakończonych.'.format(match.title))
                match.delete()
            sleep(self.worker_delay)


class NewWorker(Worker):

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        while True:
            # print(self.name)
            worker_info = WorkerInfo.objects.get(name='NewWorker')
            if worker_info.last_run < dt.now() - timedelta(hours=24):
                with NewMatchScraper() as scraper:
                    new_matches_links = scraper.get_links()
                print('Znaleziono {} nowych meczy'.format(len(new_matches_links)))
                for link in new_matches_links:
                    new_match = Match()
                    with MatchPageScraper(link) as scraper:
                        match_info = scraper.get_match_info()
                        for key, value in match_info.items():
                            setattr(new_match, key, value)
                        new_match.bets.append(scraper.get_bets())
                    new_match.save()
                    print('Dodano nowy mecz: {}'.format(new_match.title))
                worker_info.last_run = dt.now(tz('UTC'))
                worker_info.save()
            sleep(self.worker_delay)


