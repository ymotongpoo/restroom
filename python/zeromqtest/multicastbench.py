# -*- coding: utf-8 -*-

import zmq
from zmq.eventloop import ioloop
import socket
import time

#pgm_transport = "pgm://en1;224.0.0.0:5555"
pgm_transport = "tcp://127.0.0.1:5555"

def client(node_id):

  def sub_handler(socket, events):
    message = socket.recv()
    print "[node %s] message received: %s" % (node_id, message)

  context = zmq.Context()
  subscriber = context.socket(zmq.SUB)
  subscriber.connect("tcp://127.0.0.1:5555")

  while True:
    message = subscriber.recv()
    print "[node %s] message received: %s" % (node_id, message)
    time.sleep(0.1)

  """
  loop = ioloop.IOLoop.instance()
  loop.add_handler(subscriber, sub_handler, zmq.POLLIN)
  loop.start()
  """

def server():
  context = zmq.Context()
  publisher = context.socket(zmq.PUB)
  publisher.bind("tcp://*:5555")

  time.sleep(3.0)

  for i in range(100):
    message = "message %d, time: %s" % (i, time.strftime("time: %H:%M:%S"))
    print message
    publisher.send(message)
    time.sleep(1.0)


if __name__ == '__main__':
  import sys
  if sys.argv[1] == 'server':
    server()
  elif sys.argv[1] == 'client':
    client(sys.argv[2])

  
  
  
