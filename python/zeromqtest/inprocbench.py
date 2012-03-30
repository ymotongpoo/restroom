# -*- coding: utf-8 -*-

import zmq
import threading
import time
from random import randint

inproc_transport = "inproc://test"

max_trial = 100
num_threads = 10

context = zmq.Context()

def server():
  response = context.socket(zmq.REP)
  response.bind(inproc_transport)
  
  time.sleep(2.0)
  for i in range(max_trial):
    message = response.recv()
    print "received: %s" % message
    response.send(time.strftime("%H:%M:%S"))
    time.sleep(0.05)


def client(node_id):
  request = context.socket(zmq.REQ)
  request.connect(inproc_transport)
  
  for i in range(max_trial / num_threads):
    message = "id: %d, time: %s" % (node_id, time.strftime("%H:%M:%S"))
    request.send(message)
    reply = request.recv()
    print "resopnse: %s" % reply
    time.sleep(0.1)
    

server_t = threading.Thread(target=server)
server_t.daemon = True
server_t.start()

for i in range(num_threads):
  client_t = threading.Thread(target=client, args=(i, ))
  client_t.daemon = True
  client_t.start()

server_t.join()
print "done."


