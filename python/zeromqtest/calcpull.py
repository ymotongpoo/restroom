# -*- coding: utf-8 -*-

import zmq
import sys
import time

cxt = zmq.Context()
receiver = cxt.socket(zmq.PULL)
receiver.connect("tcp://127.0.0.1:5555")

sum = 0
while True:
  message = receiver.recv()
  sum += int(message)
  print "worker %s: sum = %d" % (sys.argv[1], sum)
  time.sleep(0.1)
