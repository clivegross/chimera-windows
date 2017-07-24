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
    * Write the class

"""
import win32service  
import win32serviceutil  
import win32event
import time
  
class PySvc(win32serviceutil.ServiceFramework):  
    # you can NET START/STOP the service by the following name  
    _svc_name_ = "PySvc"  
    # this text shows up as the service name in the Service  
    # Control Manager (SCM)  
    _svc_display_name_ = "Python Test Service"  
    # this text shows up as the description in the SCM  
    _svc_description_ = "This service writes stuff to a file"  
      
    def __init__(self, args):  
        win32serviceutil.ServiceFramework.__init__(self,args)  
        # create an event to listen for stop requests on  
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
      
    # core logic of the service     
    def SvcDoRun(self):  
        import servicemanager  
          
        f = open('c:\\test.dat', 'w+')  
        rc = None  
          
        # if the stop event hasn't been fired keep looping  
        while rc != win32event.WAIT_OBJECT_0:  
            f.write('TEST DATA\n')  
            f.flush()  
            # block for 5 seconds and listen for a stop event  
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)  
              
        f.write('SHUTTING DOWN\n')  
        f.close()  
      
    # called when we're being shut down      
    def SvcStop(self):  
        # tell the SCM we're shutting down  
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        # fire the stop event  
        win32event.SetEvent(self.hWaitStop)  


def do_something():
    f = open('c:\\test.dat', 'w+')  
    # rc = None  
      
    # if the stop event hasn't been fired keep looping  
    while True:  
        f.write('TEST DATA\n')  
        f.flush()
        # block for 5 seconds and listen for a stop event  
        time.sleep(5)
          
    f.write('SHUTTING DOWN\n')  
    f.close()  

if __name__ == '__main__':
    as_service = True
    if as_service:
        win32serviceutil.HandleCommandLine(PySvc)
    else:
        do_something()