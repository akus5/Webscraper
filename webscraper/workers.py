from multiprocessing import Process
from time import sleep
from datetime import datetime as dt, timedelta
from threading import Thread

from webscraper.models import Match


class Worker(Process):

    def __init__(self, worker_delay, model, data_delay=10, name='Worker'):
        super(Worker, self).__init__()
        self.worker_delay = worker_delay
        self.data_delay = data_delay
        self.name = name
        self.model = model
        self.data_provider = None

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = DataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            print(self.name)
            for item in self.data_provider.data:
                # TODO update bids
                pass
            print('Jest {} meczy'.format(len(self.data_provider.data)))
            sleep(self.worker_delay)


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
            self.model.objects(match_date__gte=dt.now(), match_date__lte=dt.now() + timedelta(days=1))

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = self.TodayDataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            print(self.name)
            for item in self.data_provider.data:
                # TODO update bids
                pass
            print('Jest {} meczy'.format(len(self.data_provider.data)))
            sleep(self.worker_delay)


class CurrentWorker(Worker):

    class CurrentDataProvider(DataProvider):

        def update(self):
            self.model.objects(match_date__gte=dt.now(), match_date__lte=dt.now() + timedelta(days=1))

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = self.CurrentDataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            print(self.name)
            for item in self.data_provider.data:
                # TODO update bids
                pass
            print('Jest {} meczy'.format(len(self.data_provider.data)))
            sleep(self.worker_delay)


class WeekWorker(Worker):

    class WeekDataProvider(DataProvider):

        def update(self):
            self.model.objects(match_date__gte=dt.now() + timedelta(days=1))

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        self.data_provider = self.WeekDataProvider(self.data_delay, self.model, self.name)
        self.data_provider.start()
        self.data_provider.update()
        while True:
            print(self.name)
            for item in self.data_provider.data:
                # TODO update bids
                pass
            print('Jest {} meczy'.format(len(self.data_provider.data)))
            sleep(self.worker_delay)


class SearchWorker(Worker):

    def run(self):
        print('Running {} on PID {}'.format(self.name, self.pid))
        while True:
            print(self.name)
            data = self.model.objects.all()
            # TODO find new matches
            print('Jest {} meczy'.format(len(data)))
            sleep(self.worker_delay)


if __name__ == '__main__':
    today_worker = TodayWorker(data_delay=15*60, worker_delay=10*60, model=Match, name='Today Worker')
    current_worker = CurrentWorker(data_delay=15, worker_delay=10, model=Match, name='Current Worker')
    week_worker = WeekWorker(data_delay=15*60, worker_delay=60*30, model=Match, name='Week Worker')
    search_worker = SearchWorker(worker_delay=60*60, model=Match, name='Search Worker')
    today_worker.start()
    current_worker.start()
    week_worker.start()
    search_worker.start()



