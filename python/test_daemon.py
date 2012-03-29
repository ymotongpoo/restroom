# -*- coding: utf-8 -*-

import time
from datetime import datetime
import os
import os.path
import daemon
import lockfile

def daemon_process():
  while True:
    print( "pid: %d, ppid: %d, time: %s" % 
           (os.getpid(), os.getppid(), datetime.now()) )
    time.sleep(5)

context = daemon.DaemonContext(
  stdout = open("stdout_file.log", "a+")
)

with context:
  daemon_process()
