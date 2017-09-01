'''Usage : python celery_beat_service.py install (start / stop / remove)
Run celery as a Windows service
'''
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import subprocess
import sys
import os
import shlex
import logging
import time

# The directory for celery.log and celery_service.log
# Default: the directory of this script
INSTDIR = os.path.dirname(os.path.realpath(__file__))
# The path of python Scripts
# Usually it is in PYTHON_INSTALL_DIR/Scripts. e.g.
# r'C:\Python27\Scripts'
# If it is already in system PATH, then it can be set as ''
PYTHONSCRIPTPATH = r'C:\Python27\Scripts'
# The directory name of django project
# Note: it is the directory at the same level of manage.py
# not the parent directory
PROJECTDIR = 'sican'

logging.basicConfig(
    filename = os.path.join(INSTDIR, 'daphne_service.log'),
    level = logging.DEBUG, 
    format = '[%(asctime)-15s: %(levelname)-7.7s] %(message)s'
)

class DaphneService(win32serviceutil.ServiceFramework):
   
    _svc_name_ = "Daphne"
    _svc_display_name_ = "Daphne Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)           

    def SvcStop(self):
        logging.info('Stopping {name} service ...'.format(name=self._svc_name_))        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        sys.exit()           

    def SvcDoRun(self):
        logging.info('Starting {name} service ...'.format(name=self._svc_name_))
        os.chdir(INSTDIR) # so that proj worker can be found
        logging.info('cwd: ' + os.getcwd())
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        command = 'daphne -b 0.0.0.0 -p 8000 sican.asgi:channel_layer'
        logging.info('command: ' + command)
        args = shlex.split(command)
        proc = subprocess.Popen(args)
        logging.info('pid: {pid}'.format(pid=proc.pid))
        self.timeout = 3000
        while True:
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                # stop signal encountered
                # terminate process 'proc'
                PROCESS_TERMINATE = 1
                handle = win32api.OpenProcess(PROCESS_TERMINATE, False, proc.pid)
                win32api.TerminateProcess(handle, -1)
                win32api.CloseHandle(handle)                
                break
                  
if __name__ == '__main__':
   win32serviceutil.HandleCommandLine(DaphneService)