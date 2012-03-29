# -*- coding: utf-8 -*-

import zmq
from random import randint, seed
import time

context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

_ = raw_input("Press enter when the workers are ready:")
print "Sending tasks to workers..."

sink.send("0")

seed()
total_msec = 0
for task_number in range(100):
  workload = randint(1, 100)
  total_msec += workload
  sender.send(str(workload))

print "Total expected cost: %d msec" % total_msec
time.sleep(1.0)
  

