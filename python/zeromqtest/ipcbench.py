# -*- coding: utf-8 -*-

import zmq
import time

max_receive = 100000 

tcp_transport = "tcp://127.0.0.1:5555"
ipc_transport = "ipc://test.ipc"

dict_transport = {
  'tcp': tcp_transport,
  'ipc': ipc_transport,
  'inproc': inproc_transport
}

def server(transport):
  cxt = zmq.Context()
  rep = cxt.socket(zmq.REP)
  rep.bind(transport)

  start_time = time.time()
  while True:
    _ = rep.recv()
    rep.send("")


def client(transport):
  cxt = zmq.Context()
  req = cxt.socket(zmq.REQ)
  req.connect(transport)

  start_time = time.time()
  for i in range(max_receive):
    req.send("")
    _ = req.recv()
  end_time = time.time()

  print "Time Elapsed: %f msec" % ((end_time - start_time) * 1000)


if __name__ == '__main__':
  import sys
  
  transport = dict_transport.get(sys.argv[1], 'tcp')

  if sys.argv[2] == 'server':
    server(transport)
  elif sys.argv[2] == 'client':
    client(transport)
  else:
    print "please assign option: 'server' or 'client'"
  
    
