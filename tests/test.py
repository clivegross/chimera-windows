# test.py
import os
import configparser
from rclone_cloud import Cloud
from backup_job import BackupJobConfigParser, BackupLogger
from rclone_cloud import Cloud


# NEED TO SET THESE EXPLICITLY SO FROZEN EXE CAN FIND CONFIG
DATA_DIR = "%programdata%\\chimera\\"
CONFIG_FILE = "config.ini"

def make_dir(path):
	abspath = get_abspath_programdata(path)
	if not os.path.exists(abspath):
			os.makedirs(abspath)
			
def get_abspath_programdata(path):
	return path.lower().replace('%programdata%', os.environ['ProgramData'])


################################################################
# need to make ProgramData directory if doesn't exist
make_dir(DATA_DIR)

# create ConfigParser object
config = configparser.ConfigParser()

# read in config from config files
master_config_file = get_abspath_programdata(DATA_DIR) + CONFIG_FILE
config.read(master_config_file)

config.read(master_config_file)

jobs_dir = get_abspath_programdata(config.get('paths', 'jobs'))

# read in job configs from jobs dir
for f in os.listdir(jobs_dir):
    if f.endswith(".ini"):
        config.read(os.path.join(jobs_dir, f))

# create logger object
logger = BackupLogger(get_abspath_programdata(config.get('logging', 'file')))
# create job_creator object
backup_job_creator = BackupJobConfigParser(config)
# empty list to hold all job instances
all_jobs = list()
# populate all_jobs
for section in config.sections():
    if section.startswith('job'):
        all_jobs.append(section)

# empty list to hold all enabled job instances
enabled_jobs = list()
# populate enabled_jobs
for job_name in all_jobs:
    job = backup_job_creator.create_job(job_name, logger=logger)
    if job.is_enabled():
        enabled_jobs.append(job)
        

        
# s3 = Cloud('rclone-medusa')
# command = [
    # 'rclone',
    # 'copy',
    # '--config=C:\\ProgramData\\chimera\\config.ini',
    # '-v',
    # 'C:\\ProgramData\\medusa-agent\\sitedata',
    # 'rclone-medusa:sitedata_20170531_003900190061'
# ]


for job in enabled_jobs:
    job.run()