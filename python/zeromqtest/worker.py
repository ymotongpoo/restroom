# -*- coding: utf-8 -*-

import zmq
import time

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

while True:
  message = receiver.recv()
  print "%s." % message

  time.sleep(int(message) * 0.001)
  sender.send("")


  
