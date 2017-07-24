from datetime import datetime as dt
import time
import logging
from logging.handlers import RotatingFileHandler
from sys import exc_info
import os
from app.shell import shell_command
from app.email_client import EmailClient
from app.rclone_cloud import Cloud
from app.crontab import CronTab
from app.zipper import zipper


LOGLEVEL_LOOKUP = [
    'Emergency',
    'Alert',
    'Critical',
    'Error',
    'Warning',
    'Notice',
    'Informational',
    'Debug'
]


class BackupJob(object):

    def __init__(self):
        """
        sync: if True, use rclone sync instead of rclone copy
        compress: if True, compress source to zip file first
        """
        self.logger = None
        self.notifier = None
        self.sync = False
        self.compress = False
        self.has_before_dependency = False
        self.has_after_dependency = False
        self.has_prefix = False

    def set_name(self, name):
        """
        set job name
        """
        self.name = name

    def set_source(self, source):
        self.source = source

    def set_dest(self, dest, append_datetime=True, prefix=None):
        """
        set backup destination.
        dest: the destination path on the remote (str)
        append_datetime: should the destination file/dir filename have
            '_<current_datetme>' appended? (bool)
        """
        self.dest = dest
        if prefix is not None:
            self.has_prefix = True
            self.prefix = prefix
        self.append_datetime = append_datetime

    def set_enabled(self, enabled):
        """
        set job enabled state to True or False
        """
        self.enabled = enabled

    def is_enabled(self):
        """
        use to query if job is enabled
        """
        return self.enabled

    def set_cloud(self, remote, bucket=None, config=None):
        self.remote = remote
        self.cloud = Cloud(self.remote, bucket=bucket, config=config)

    def set_crontab(self, crontab):
        """
        parmas:
         crontab:
            A crontab-like representation of the backup schedule.
            This could be used to write directly to crontab or handled within python.
            eg. "0 0 * * * *"
         schedule:
            An instance of CronTab using crontab as the schedule.
        """
        self.crontab = crontab
        self.schedule = CronTab(crontab)

    def set_sync(self, do_sync=False):
        """
        sync instead of copy
        """
        self.sync = do_sync

    def set_email_notifier(self, host, port, username, password, sender, recipients):
        self.notifier = BackupNotifier(host, port, username, password, sender, recipients)

    def set_logger(self, logger, loglevel=3):
        """
        pass in an instance of BackupLogger() for logging
        """
        self.logger = logger
        self.logger.set_loglevel = loglevel

    def set_compress(self, compress=False, zipdir='/tmp'):
        """
        if compress true then compress source to a zipfile
        """
        self.compress = compress
        self.zipdir = zipdir

    def zip_source(self):
        """
        make zip file for copying to remote
        """
        self.set_zipfile()
        zipper(self.source, self.abszipfile)

    def set_zipfile(self):
        suffix = ""
        if self.append_datetime:
            suffix += dt.now().strftime('_%Y%m%d_%H%M%S%f')
        suffix += '.zip'
        self.zipfile = self.source.split('/')[-1] + suffix
        self.abszipfile = self.zipdir + '/' + self.zipfile

    def rm_source_zip(self):
        """
        need to rm the source zip file after the transfer is complete
        """
        os.remove(self.abszipfile)

    def set_dependency(self, command, before=True):
        """
        pass in a string shell command to be executed before backup job
        or after backup job (before=True/False)

        breaks command string into list for subprocess.Popen

        """
        if before:
            self.has_before_dependency = True
            self.before_command = command.split()
        else:
            self.has_after_dependency = True
            self.after_command = command.split()

    def run(self):
        """
        run backup job.
        if append_datetime True, append the current datetime to end of
        destination file/dir

        TODO:
        - break this function up better, its yuck
        - write entries to log thoughout this functions execution, rather than
            waiting til run fininshed
        - fix bandaid for append datetime and compress both being true
        """
        if self.enabled:
            output = ""
            ################################
            # compress to zip if required
            # flag to remove temporary source zipfile
            do_rm_zip = False
            # if compress == True, make a zip file first
            try:
                if self.compress:
                    self.zip_source()
                    source = self.abszipfile
                    do_rm_zip = True
                else:
                    source = self.source
            except:
                output += "\n" + str(dt.now()) + ": Failed to compress source into zipfile\n"
                output += str(exc_info()[0])
            ################################
            # do exec before dependency
            # do rclone upload
            # do exec after dependency
            # handle results
            try:
                # execute before dependency program before job run
                if self.has_before_dependency:
                    before_output = shell_command(self.before_command)
                    output += '###########\nbefore dependency:\n'
                    output += str(self.before_command) + '\n'
                    output += before_output
                # this workaround is poo!
                if self.append_datetime and not self.compress:
                    dest = self.dest + dt.now().strftime('_%Y%m%d_%H%M%S%f')
                else:
                    dest = self.dest
                # add prefix 
                if self.has_prefix:
                    dest = self.prefix + '_' + dest
                # check if set to rclone sync not copy
                if self.sync:
                    rclone_output = self.cloud.sync(source, dest)
                else:
                    rclone_output = self.cloud.copy(source, dest)
                output += '###########\nbackup job:\n'
                output += rclone_output
                # execute after dependency program after job run
                if self.has_after_dependency:
                    after_output = shell_command(self.after_command)
                    output += '###########\nafter dependency:\n'
                    output += str(self.after_command) + '\n'
                    output += after_output
                    
                self.handle_result(after_output)
            except:
                output += str(exc_info()[0])
            try:
                if do_rm_zip:
                    self.rm_source_zip()
            except:
                output += str(exc_info()[0])

        else:
            output = " ".join([
                "Backup job",
                job.name,
                "attempted to run but the job is not enabled",
                "(job.enabled = False)",
                "Nothing was done."
            ])
        self.handle_result(output)

    def handle_result(self, output):
        """
        currently only supports loglevels of 3 (error) or 7 (debug)
        based on job result:
         - write to log
         - send email
        """
        # TO DO code this up so it works
        record = BackupRecord(self, output)
        if record.has_errors:
            errorlevel = 3
        else:
            errorlevel = 7
        # write result to log
        if self.logger.enabled:
            self.logger.write(record.message)
        # email result
        if errorlevel <= self.logger.loglevel:
            if self.notifier.enabled:
                self.notifier.notify_by_email(record.message, record.subject)
                # log email transmission
                self.logger.write(str(time.asctime()) + ": An email was sent.")


class BackupRecord(object):

    def __init__(self, job, output):
        """
        an object representing the result of a backup job.
        used for handling the backup job result, eg:
         - logging
         - alert notifications (emails)
        """
        self.job = job
        self.result = output
        self.check_has_errors()
        self.make_record()
        self.make_subject()
        

    def check_has_errors(self):
        """
        Failsafe check of rclone copy output for errors.
        Unless output explicitly contains a row reading:

        Errors:     0

        Assume has_errors = True.

        TODO:
        Should decouple this from rclone

        """
        # set has_errors to True
        # stdout/stderr content must prove that has_erros = False
        # this may miss some errors
        has_errors = False
        for row in self.result.split('\n'):
            if 'Errors:' in row:
                # weirdly handled in windows this is a byte but also a string
                # cant decode to utf-8 becuase already type str?
                # str.split() doesnt split newlines \\n so I replace newlines with spaces here
                # I think im missing something obvious
                row_str = row.replace("\\n", ' ')
                # check rclone output for "Errors:    x", if x = 0 presume no errors
                i = [i for i, s in enumerate(row_str.split()) if 'Errors:' in s][0] + 1
                try:
                    error_count = int(row_str.split()[i])
                    if error_count == 0:
                        has_errors = False
                    else:
                        has_errors = True
                except:
                    pass
        
        self.has_errors = has_errors

    def make_record(self):
        message = ""
        message += "JOB STARTED"
        message += "\ntime: " + str(time.asctime())
        message += "\nname: '" + self.job.name + "'."
        message += "\nsource: " + self.job.source
        message += "\ndestination: " + self.job.remote + ':' + '{BUG: FIX UP THE DEST}' + self.job.dest
        message += "\nhas errors: " + str(self.has_errors)
        message += "\noutput:\n" + self.result
        self.message = message

    def make_subject(self):
        subject = "".join([
        "Backup job ",
        self.job.name,
        " to ",
        self.job.remote,
        ':',
        self.job.dest
        ])
        self.subject = subject


class BackupLogger(object):

    def __init__(self, logfile, loggername='chimera', loglevel=6, maxBytes=1024*1024*2, backupCount=10):
        logger = logging.getLogger(loggername)
        logger.setLevel(logging.DEBUG)
        self.logfile = logfile
        handler = RotatingFileHandler(self.logfile, maxBytes=maxBytes, backupCount=backupCount)
        logger.addHandler(handler)
        self.set_loglevel(loglevel)
        self.logger = logger
        self.enabled = True

    def set_enabled(self, enabled):
        """
        enable or disable logging
        """
        self.enabled = enabled

    def write(self, entry, level=7):
        if self.enabled:
            if level == 7:
                self.logger.debug(entry)
            else:
                self.logger.error(entry)

    def set_loglevel(self, level=3):
        """
        The list of severities is defined by RFC 5424:
        See https://en.wikipedia.org/wiki/Syslog
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        Value   Severity    Description
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        0       Emergency   System is unusable.
        1       Alert 		Action must be taken immediately.
        2       Critical    Critical conditions, such as hard device errors.
        3       Error       Error conditions.
        4       Warning     Warning conditions.
        5       Notice      Normal but significant conditions.
        6       Informational Informational messages.
        7       Debug       Debug-level messages.
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        """
        if level > 7:
            self.loglevel = 7
        elif level < 0:
            self.loglevel = 0
        else:
            self.loglevel = int(level)




class BackupNotifier(EmailClient):

    def __init__(self,  host, port, username, password, sender, recipients):
        """
        wrapper for EmailClient()
        """
        self.set_host(host, port)
        self.set_auth(username, password)
        self.set_sender(sender)
        self.set_recipients(recipients)
        self.enabled = True

    def notify_by_email(self, message, subject):
        if self.enabled:
            self.write_message(body=message, subject=subject)
            self.sendmail()

    def set_enabled(self, enabled):
        """
        enable or disable notifier
        """
        self.enabled = enabled


class BackupJobConfigParser(object):
    """
    object used to transform a backup job config file
    to a BackupJob object
    """

    def __init__(self, config):
        self.config = config

    def get_config(self, section, option, default=None, boolean=False):
        """
        safely get config, if config section/option missing, use a default option

        section: ConfigParser object 'section'
        option: ConfigParser object 'option' in 'section'
        deafult: the default value to use if option missing from config
        boolean: if True, use getboolean() instead of get() to prevent returning str
        """
        if self.config.has_option(section, option):
            if boolean:
                # if option needs a bool value, use getboolean() instead
                config_option = self.config.getboolean(section, option)
            else:
                config_option = self.config.get(section, option)
        else:
             config_option = default
        return config_option

    def get_abspath_programdata(self, path):
        """
        clean up system variable path conversion to absolute path
        
        TODO:
         * this is a duplicate function of manager. consolidate so this method is only written once.
        """
        # python 2.7 doesnt parse % the same way, have added some extra 'replaces' to cover all possibilities
        return path.lower().replace('%%programdata%%', os.environ['ProgramData']).replace('%programdata%', os.environ['ProgramData']).replace('%','')
        
    def create_job(self, job_name, logger=None):
        """
        create backup job from config file
        """
        job = BackupJob()
        job.set_name(job_name)
        job.set_cloud(
            self.get_config('rclone', 'remote'),
            config=self.get_abspath_programdata(self.get_config('rclone', 'config')),
            bucket=self.get_config('rclone', 'bucket')
        )
        job.set_source(self.get_abspath_programdata(self.get_config(job_name, 'source', default="")))
        job.set_dest(
            self.get_config(job_name, 'dest', default=""),
            self.get_config(job_name, 'append_datetime', default=True, boolean=True),
            prefix=self.get_config(job_name, 'prefix', default=False)
        )
        job.set_compress(
            self.get_config(job_name, 'compress', default=False, boolean=True),
            zipdir = "/data"
        )
        job.set_enabled(self.get_config(job_name, 'enabled', True, True))
        job.set_crontab(self.get_config(job_name, 'schedule', default="0 0 0 * *"))
        job.set_logger(
            logger,
            self.get_config(job_name, 'loglevel', default="3")
        )
        job.set_email_notifier(
            self.get_config('email', 'host'),
            self.get_config('email', 'port'),
            self.get_config('email', 'username'),
            self.get_config('email', 'password'),
            self.get_config('email', 'sender'),
            self.get_config('email', 'recipients')
        )
        # set before and after program dependencies
        depend_before = self.get_config(job_name, 'depend_before')
        depend_after = self.get_config(job_name, 'depend_after')
        if depend_before:
            job.set_dependency(depend_before, before=True)
        if depend_after:
            job.set_dependency(depend_after, before=False)

        return job


class JobLoader(object):

    def __init__(self, config, jobs_dir, logger):
        self.jobs_dir = jobs_dir
        self.logger = logger
        self.config = config
    
    def load(self):
        # read in job configs from jobs dir
        for f in os.listdir(self.jobs_dir):
            if f.endswith(".ini"):
                self.config.read(os.path.join(self.jobs_dir, f))

        # create job_creator object
        backup_job_creator = BackupJobConfigParser(self.config)
        # empty list to hold all job instances
        all_jobs = list()
        # populate all_jobs
        for section in self.config.sections():
            if section.startswith('job'):
                all_jobs.append(section)

        # empty list to hold all enabled job instances
        enabled_jobs = list()
        # populate enabled_jobs
        self.logger.write(str(time.asctime()) + ": " + str(len(all_jobs)) + " jobs available.")
        for job_name in all_jobs:
            try:
                job = backup_job_creator.create_job(job_name, logger=self.logger)
                if job.is_enabled():
                    enabled_jobs.append(job)
                    self.logger.write(str(time.asctime()) + ": Job '" + job_name + "' added.")
                else:
                    self.logger.write(str(time.asctime()) + ": Job '" + job_name + "' won't be added because it is not enabled.")
            except:
                self.logger.write(str(time.asctime()) + ": Failed to create job for '" + job_name + "'.")
                
        return enabled_jobs