from multiprocessing import Process
from time import sleep
from datetime import datetime as dt, timedelta
from threading import Thread

from webscraper.models import Match


class TodayWorker(Process):

    def __init__(self):
        super(TodayWorker, self).__init__()
        self.updater = None

    def start(self):
        super().start()

    def run(self):
        print('Running Today Worker on PID {}'.format(self.pid))
        self.updater = self.Updater()
        self.updater.start()
        while True:
            print('Today Worker')
            # print(len(self.updater.today_matches))
            for match in self.updater.today_matches:
                # TODO update bids
                pass
            sleep(5)

    class Updater(Thread):
        today_matches = []

        def __init__(self):
            super().__init__()
            self.today_matches = []
            self.setName('Today matches updater')

        def update(self):
            self.today_matches = Match.objects(match_date__lte=dt.now() + timedelta(days=1))
            print('Update today matches list')
            # print('updated  = {}'.format(self.today_matches))

        def run(self):
            from os import getpid
            print('Running thread {} on process {}'.format(self.getName(), getpid()))
            while True:
                self.update()
                sleep(15)


class CurrentWorker(Process):

    def __init__(self):
        super(CurrentWorker, self).__init__()
        self.updater = None

    def start(self):
        super().start()

    def run(self):
        print('Running Current Worker on PID {}'.format(self.pid))
        self.updater = self.Updater()
        self.updater.start()
        while True:
            print('Current Worker')
            # print(len(self.updater.today_matches))
            for match in self.updater.current_matches:
                # TODO update bids
                pass
            sleep(5)

    class Updater(Thread):
        current_matches = []

        def __init__(self):
            super().__init__()
            self.current_matches = []
            self.setName('Current matches updater')

        def update(self):
            self.current_matches = Match.objects(match_date__lte=dt.now(), match_date__gte=dt.now() - timedelta(minutes=90))
            print('Update current matches list')
            # print('updated  = {}'.format(self.today_matches))

        def run(self):
            from os import getpid
            print('Running thread {} on process {}'.format(self.getName(), getpid()))
            while True:
                self.update()
                sleep(15)


if __name__ == '__main__':
    today_worker = TodayWorker()
    current_worker = CurrentWorker()

    today_worker.start()
    # today_worker.join()

    current_worker.start()
    # current_worker.join()

