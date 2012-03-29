# -*- coding: utf-8 -*-

import zmq
import time

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

message = receiver.recv()

start_time = time.time()
for task_number in range(0, 100):
  message = receiver.recv()
  if task_number % 10 == 0:
    print ":"
  else:
    print "."

end_time = time.time()    

print "Total elapsed time: %f msec" % ((end_time - start_time) * 1000)
