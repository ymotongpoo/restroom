# -*- coding: utf-8 -*-

import threading
import time

def print_workload(node, tasks):
  print "node id=%d, tasks=%d" % (node, tasks)

def process(node, tasks):
  print_workload(node, tasks)
  while tasks > 0:
    tasks -= 1
    print_workload(node, tasks)
    time.sleep(0.2)

for i in range(1, 6):
  t = threading.Thread(target=process, args=(i, i*5))
  t.start()

print "thread processing..."
t.join()
print "threading done"


