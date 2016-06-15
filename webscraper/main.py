from webscraper.workers import TodayWorker, CurrentWorker, WeekWorker, NewWorker, EndedWorker
from webscraper.models import Match


if __name__ == '__main__':
    today_worker = TodayWorker(data_delay=15*60, worker_delay=10*60, model=Match, name='Today Worker')
    current_worker = CurrentWorker(data_delay=60, worker_delay=2*60, model=Match, name='Current Worker')
    week_worker = WeekWorker(data_delay=15*60, worker_delay=30*60, model=Match, name='Week Worker')
    new_worker = NewWorker(worker_delay=60*60, model=Match, name='New Worker')
    ended_worker = EndedWorker(worker_delay=30*60, model=Match, name='Ended Worker')
    today_worker.start()
    current_worker.start()
    week_worker.start()
    new_worker.start()
    ended_worker.start()
