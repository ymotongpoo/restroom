# -*- coding: utf-8 -*-

import zmq
import time

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

message = receiver.recv()

start_time = time.clock()
for task_number in range(0, 100):
  message = receiver.recv()
  if (task_number / 10) * 10 == task_number:
    print ":"
  else:
    print "."

print "Total elapsed time: %f msec" % ((time.clock() - start_time) * 1000)
