# -*- coding: utf-8 -*-

import zmq
from zmq.eventloop import ioloop
import socket
import time

#pgm_transport = "pgm://en1;224.0.0.0:5555"
pgm_transport = "pgm://en0;239.193.0.0:5555"

def client(node_id):
  def sub_handler(socket, events):
    message = socket.recv()
    print "[node %s] message received: %s" % (node_id, message)

  context = zmq.Context()
  subscriber = context.socket(zmq.SUB)
  subscriber.connect(pgm_transport)
  subscriber.setsockopt(zmq.SUBSCRIBE, "")

  loop = ioloop.IOLoop.instance()
  loop.add_handler(subscriber, sub_handler, zmq.POLLIN)
  loop.start()


def server():
  context = zmq.Context()
  publisher = context.socket(zmq.PUB)
  publisher.bind(pgm_transport)

  time.sleep(3.0)

  for i in range(100):
    message = "message %d, time: %s" % (i, time.strftime("time: %H:%M:%S"))
    print message
    time.sleep(1.0)
    publisher.send(message)


if __name__ == '__main__':
  import sys
  if sys.argv[1] == 'server':
    server()
  elif sys.argv[1] == 'client':
    print "client %s" % sys.argv[2]
    client(sys.argv[2])

  
  
  
