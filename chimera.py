"""winservice.py

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::
		
		# install as a service
        $ python winservice.py install
		# start service
		$ python winservice.py start

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * run each sched event as a separate thread

"""
import time
# python 2 support
try:
    import configparser # (python 3)
except ImportError:
    import ConfigParser as configparser # (python 2)
from app import Chimera


CONFIG_FILE = './config.ini'


if __name__ == '__main__':
    
    # create ConfigParser object
    config = configparser.ConfigParser()
    
    # read in config from config files
    config.read(CONFIG_FILE)
    
    # instantiate monolithic Chimera object
    chimera = Chimera(config, logfile=config.get('logging', 'file'))
    chimera.logger.write("\n" + str(time.asctime()) + ": The Chimera service was started.")
    
    # get jobs directory
    #############
    # get full path!!!!
    jobs_dir = config.get('paths', 'jobs')
    
    chimera.load_jobs(jobs_dir)
        
    chimera.schedule_jobs()
    
    buffer = 10 #seconds
    
    # loop forever
    while chimera._running:
        has_run = False
        
        for job in chimera.scheduler.queue:
            countdown = job.time - time.time()
            if countdown < buffer:
                chimera.scheduler.run()
                has_run = True
                break
        
        if has_run:
            chimera.schedule_jobs()
        
        # block for 5 seconds and listen for a stop event  
        time.sleep(5)
    
    # break to here only if loop exited
    chimera.logger.write(str(time.asctime()) + ": The Chimera service was stopped.")
    
    chimera.stop()
