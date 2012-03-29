# -*- coding: utf-8 -*-

import zmq
import time
from random import randrange

cxt = zmq.Context()
sender = cxt.socket(zmq.PUSH)
sender.bind("tcp://127.0.0.1:5555")


time.sleep(10)

sum = 0
for i in range(1000):
  value = randrange(5000)
  sum += value
  print i, value
  sender.send(str(value))

print "sum is %d" % sum
time.sleep(10)
