# -*- coding: utf-8 -*-

import zmq
import threading
import multiprocessing
import time
import random

inproc_transport = "inproc://test"

max_trial = 100
num_ = 10

context = zmq.Context()
random.seed()

def server():
  response = context.socket(zmq.REP)
  response.bind(inproc_transport)
  
  time.sleep(2.0)
  for i in range(max_trial):
    message = response.recv()
    print "received: %s" % message
    response.send(str(random.randint(100, 1000)))


def client(node_id):
  request = context.socket(zmq.REQ)
  request.connect(inproc_transport)
  
  for i in range(max_trial / num_threads):
    message = "id: %d, time: %s" % (node_id, time.strftime("%H:%M:%S"))
    request.send(message)
    reply = request.recv()
    workload = int(reply)
    print "id: %d, workload: %d msec" % (node_id, workload)
    time.sleep(workload * 0.001)
    

def test_threads():
  server_t = threading.Thread(target=server)
  server_t.daemon = True
  t_start = time.time()
  server_t.start()

  for i in range(num_threads):
    client_t = threading.Thread(target=client, args=(i, ))
    client_t.daemon = True
    client_t.start()

  server_t.join()
  t_end = time.time()
  time.sleep(1.0)
  print "Time Elapsed: %f msec." % ((t_end-t_start)*0.001)


def test_processes():
  server_p = multiprocessing.Process(target=server)
  server_p.daemon = True
  t_start = time.time()
  server_p.start()

  for i in range(num_threads):
    client_p = multiprocessing.Process(target=client, args=(i, ))
    client_p.daemon = True
    client_p.start()

  server_t.join()
  t_end = time.time()
  time.sleep(1.0)
  print "Time Elapsed: %f msec." % ((t_end-t_start)*0.001)

if __name__ == "__main__":
  #test_threads()
  test_processes()
  print "done."
