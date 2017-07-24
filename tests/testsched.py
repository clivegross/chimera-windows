# testsched.py
import sched
import time
from crontab import CronTab

crontab = '* * * * *'

def job():
    print('running job')

def next_job():
    scheduler.enter(CronTab(crontab).next(), 1, job)

scheduler = sched.scheduler(time.time, time.sleep)
next_job()

buffer = 10 #seconds

while True:
    print(scheduler.queue)
    has_run = False
    for event in scheduler.queue:
        countdown = event.time - time.time()
        print(countdown)
        if countdown < buffer:
            scheduler.run()
            has_run = True
            break
    
    if has_run:
        print('scheduling next')
        next_job()
        
    time.sleep(5)
