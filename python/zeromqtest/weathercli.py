# -*- coding: utf-8 -*-

import zmq
import sys

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")

# receive only message with zipcode being 10001
zipfilter = sys.argv if len(sys.argv) > 1 else "10001 "
subscriber.setsockopt(zmq.SUBSCRIBE, zipfilter)

update_samples = 10
for updates in range(update_samples):
  message = subscriber.recv()
  zipcode, temprature, relhumidity, message_id = message.split()
  print ("zip:%s, temp:%s, relh:%s, id:%s" % 
         (zipcode, temprature, relhumidity, message_id))
  total_temp = float(temprature)

print ("average temprature for zipcode '%s' was '%f'" % 
       (zipfilter, total_temp / update_samples))


