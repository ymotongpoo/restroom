# -*- coding: utf-8 -*-

import zmq
import time

context = zmq.Context()
responder = context.socket(zmq.REP)
responder.bind("tcp://*:5555")

while True:
  request = responder.recv()
  print "recieved request: [%s]" % request
  time.sleep(1.0)
  responder.send("World at %s" % time.strftime("%Y-%m-%dT%H:%M:%S"))
