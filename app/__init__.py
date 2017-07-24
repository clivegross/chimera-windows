# __init__.py
#
# TODO:
# comment this program thoroughly
#
import time
import sched
from app.backup_job import JobLoader, BackupLogger
from app.crontab import CronTab


class Chimera(object):

    def __init__(self, config, logfile):
        self.logger = BackupLogger(logfile)
        self.config = config
        self._running = False
    
    def run_job(self, job):
        self.logger.write("\n\n" + str(time.asctime()) + ": JOB STARTED: " + job.name)
        try:
            job.run()
        except:
            self.logger.write("\n\n" + str(time.asctime()) + ": EXCEPTION RAISED DURING JOB EXECUTION: " + job.name)

    def pretty_countdown(self, timer_secs):
        if timer_secs < 180:
            return str(int(timer_secs)) + ' seconds'
        elif timer_secs >= 180 and timer_secs < 180*60.0:
            return str(int(timer_secs/60.0)) + ' minutes'
        else:
            return str(round(timer_secs/60/60.0), 1) + ' hours'
            
    def load_jobs(self, jobs_dir):
        job_loader = JobLoader(self.config, jobs_dir, self.logger)
        self.enabled_jobs = job_loader.load()
            
    def schedule_jobs(self):
        self._running = True
        
        self.scheduler = sched.scheduler(time.time, time.sleep)
        
        for job in self.enabled_jobs:
            self.logger.write(
                str(time.asctime()) + 
                ": Job '" + job.name +
                "' next scheduled in " +
                self.pretty_countdown(CronTab(job.crontab).next())
            )
            job.next_run = self.scheduler.enter(job.schedule.next(), 1, self.run_job, (job,))

    def stop(self):
        self._running = False
        try:
            if self.scheduler:
                for job in self.enabled_jobs:
                    self.scheduler.cancel(job.next_run())
        except:
            self.logger.write("Failed to cancel events")