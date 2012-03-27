# -*- coding: utf-8 -*-

import zmq
import time
from random import randrange

context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")

message_id = 0
while True:
  zipcode     = randrange(10001, 10010)
  temprature  = randrange(0, 215) - 80
  relhumidity = randrange(0, 50) + 10

  update = "%05d %d %d %d" % (zipcode, temprature, relhumidity, message_id)
  message_id += 1
  print update
  time.sleep(1.0)
  publisher.send(update)







