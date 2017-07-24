import sched
import time
from crontab import CronTab
from datetime import datetime as dt

def print_time():
    print("Run at time: " + str(dt.now()))

scheduler = sched.scheduler(time.time, time.sleep)
entry = CronTab('*/2 * * * *')
# next_run = croniter('*/5 * * * *', base)  # every 5 minutes
# last_run_at = dt.now()

print("Started scheduler at time: " + str(dt.now()))

def do_something_again(message):
        print('RUNNING:', str(dt.now()), message)
        # Do whatever you need to do here
        # then re-register task for same time tomorrow
        scheduler.enter(entry.next(), 1, do_something_again, (message,))

while True:
    do_something_again('Running again')
    print(scheduler.queue)
    print(scheduler.empty())
    scheduler.run()
    time.sleep(5)

# for i in range(5):
#     print(entry.next())
#     time.sleep(5)
       # 2010-01-25 04:50:00
# def job(name='default'):
#     print("I'm working on " + name)
#
# schedule.every(2).minutes.do(job('every 2 minutes'))
# schedule.every().hour.do(job('every hour'))
# schedule.every().day.at('every day at 15:55').do(job)
# schedule.every().monday.do(job('monday'))
# schedule.every().saturday.at('15:52').do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
