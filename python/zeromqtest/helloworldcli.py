# -*- coding: utf-8 -*-
import zmq
import sys

context = zmq.Context()

# Socket to talk to server
print "connecting to hello world server"
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(1, 100):
  print "sending request %d ..." % request
  socket.send("Hello from %s" % sys.argv[1])

  message = socket.recv()
  print "received reply %d [ %s ]" % (request, message)

